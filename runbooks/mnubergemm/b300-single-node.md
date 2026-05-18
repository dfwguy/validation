# MNUberGEMM 72-hour burn-in — DGX B300 (single-node)

Burn-in runbook for single-node DGX B300 systems using the MNUberGEMM workload
distributed by NVIDIA's Compute Engineering team. Validated across four B300
viking lab nodes in May 2026. Workload config derived from Jeffrey Miller's
Eli Lilly LillyPod validation script, adapted to single-node (no Slurm) with
both enroot and docker container runtimes.

## Target profile

| Field | Value |
| --- | --- |
| Platform | DGX Server for DGX B300 (DGX OS 7.x, x86) |
| GPUs | 8x NVIDIA B300, 275 GB HBM each, 1100 W cap |
| Host driver | 580.69 or 580.159 series (CUDA 13.0 host runtime) |
| Container | `nvcr.io/0948245400141054/mnubergemm:tensorrt-25.12-v1.13-x86` |
| Workload | `GN` (GEMM + NCCL). The `C` / Copy Engine phase is disabled — see Gotchas. |
| Duration | 259200 s (72 h) · duty 0.9 · 8 MPI ranks |
| Runtimes supported | enroot 4.x **or** docker + nvidia-container-toolkit |

---

## Gotchas (read first)

These three traps cost ~3 hours across the first lab box. They will catch the
next person too if the host has the same DGX OS 7.x / driver 580.x baseline.

### 1. NGC 403 Forbidden on container pull

The mnubergemm container lives in NGC org `0948245400141054`, which requires
explicit org membership. NGC service keys generated under accounts that are
not members of that org will fail with `403 Forbidden` regardless of scope.

**Fix:** use a key from an account that has membership in
`0948245400141054`. If you generate a key and the org isn't in your Entity
Value dropdown, you don't have membership — ping the image owner for access
or have them mirror the image to an org you can read.

### 2. `cuInit` hangs / "no CUDA-capable device" across MPI ranks

`CUDA_VISIBLE_DEVICES=all` is parsed literally inside the container — CUDA
can't find a device named "all", and ranks 1–7 fail `cudaSetDevice(local_rank)`
during MPI init. The container runtime hook handles `all` at startup; the env
var no longer carries that semantic inside the running container.

**Fix:** `unset CUDA_VISIBLE_DEVICES` before the `mpirun` call. Each rank then
picks up its assigned GPU via `cudaSetDevice(local_rank)`.

### 3. `etbl.cpp 'invalid resource handle'` after GEMM phase

CUDA tools / CUPTI ABI mismatch — host driver 580.x (CUDA 13.0) vs container
CUDA 13.1+. Surfaces in the Copy Engine (C) phase as
`std::runtime_error` or, on newer drivers with forward-compat enabled, as
`QUAL_RUNTIME_ERROR (induced by 18)` = `cudaErrorInvalidPtx`.

**Fix:** drop `C` from the workload string. Use `--workload GN`. The real fix
is upgrading the host driver to ≥581 (full CUDA 13.2 support), which enables
`GNC` and adds DMA-path thermal coverage.

---

## 1. One-time setup

All steps run as `root` (or under `sudo`) on the B300 host.

### 1.1 Verify tooling

```bash
which enroot docker tmux nvidia-smi dcgmi mpirun
nvidia-smi -L                # expect 8x B300
cat /etc/dgx-release
df -h /                      # expect ~1+ TB free for container + logs
```

Pick the runtime path:

- **enroot present** → use [§2 enroot path](#2-enroot-path)
- **enroot missing, docker present** → use [§3 docker path](#3-docker-path).
  Also verify the NVIDIA runtime is registered with Docker:

  ```bash
  docker info 2>/dev/null | grep -i runtime
  ```

  If `nvidia` is not listed but `nvidia-ctk` is installed:

  ```bash
  nvidia-ctk runtime configure --runtime=docker
  systemctl restart docker
  docker run --rm --gpus all ubuntu:24.04 nvidia-smi -L  # confirm 8 GPUs pass through
  ```

### 1.2 Working directory

```bash
mkdir -p ~/mnubergemm-logs
```

### 1.3 NGC credentials

Replace `<NGC-KEY>` with a service key generated under an account that is a
member of org `0948245400141054`. `$oauthtoken` is **literal** — leave it as
`$oauthtoken` in the credentials file; do not substitute it with the key.

**For enroot:**

```bash
mkdir -p ~/.config/enroot
cat > ~/.config/enroot/.credentials <<'EOF'
machine nvcr.io login $oauthtoken password <NGC-KEY>
EOF
chmod 600 ~/.config/enroot/.credentials
```

**For docker:**

```bash
echo '<NGC-KEY>' | docker login nvcr.io -u '$oauthtoken' --password-stdin
```

> Rotate the NGC key at `ngc.nvidia.com` → Service Keys when the burn
> completes. The container is staged locally as a .sqsh (enroot) or in the
> docker image store, so revoking the key does not affect running burns or
> future relaunches from the local image.

---

## 2. Enroot path

### 2.1 Pull and create

```bash
cd ~/mnubergemm-logs
enroot import -o mnubergemm-v1.13.sqsh \
  'docker://nvcr.io#0948245400141054/mnubergemm:tensorrt-25.12-v1.13-x86'

enroot create --name mnubergemm ~/mnubergemm-logs/mnubergemm-v1.13.sqsh
enroot list                  # confirm 'mnubergemm' is listed
```

### 2.2 Smoke test (60 s)

**Terminal A — run the test:**

```bash
enroot start --rw --mount $HOME/mnubergemm-logs:/logs mnubergemm bash -c '
  cd /opt/mnubergemm
  unset CUDA_VISIBLE_DEVICES
  export NCCL_DEBUG=WARN
  export NCCL_P2P_LEVEL=NVL
  export NCCL_IB_DISABLE=1
  export NCCL_NVLS_ENABLE=0
  mpirun -np 8 --allow-run-as-root --bind-to none --map-by slot \
    --output-filename /logs/ranks-test \
    ./mnubergemm --time_to_run 60 --dynamic_adj \
      --MM_max_workload 65536 --max_workload 65536 \
      --workload GN --duty 0.9 \
      --MM_sm_count 112 --NET_sm_count 32 \
  2>&1 | tail -20
'
```

**Terminal B — watch GPUs ramp:**

```bash
watch -n 2 'nvidia-smi --query-gpu=index,utilization.gpu,power.draw,temperature.gpu --format=csv'
```

**Pass criteria:** within ~45 s all 8 GPUs ramp toward 95–100 % util and
~1000 W. Final log lines include `RANK PERF G` / `RANK PERF N` across 8
ranks, `GLOBAL PERF`, `returning QUAL_OK`, and
`XID MONITOR : found []`.

### 2.3 Launch the 72-hour burn

```bash
tmux new-session -d -s mnubergemm "enroot start --rw \
  --mount $HOME/mnubergemm-logs:/logs mnubergemm bash -c \
  'cd /opt/mnubergemm && unset CUDA_VISIBLE_DEVICES && \
   export NCCL_DEBUG=WARN NCCL_P2P_LEVEL=NVL NCCL_CUMEM_ENABLE=1 \
          NCCL_CUMEM_HOST_ENABLE=0 NCCL_IB_DISABLE=1 NCCL_MIN_CTAS=64 \
          NCCL_NVLS_ENABLE=0 && \
   mpirun -np 8 --allow-run-as-root --bind-to none --map-by slot \
     --output-filename /logs/ranks-72h \
     ./mnubergemm --dynamic_adj \
       --MM_max_workload 65536 --max_workload 65536 \
       --time_to_run 259200 --workload GN --duty 0.9 \
       --MM_sm_count 112 --NET_sm_count 32 \
   2>&1 | tee /logs/burn-72h-\$(date +%Y%m%d-%H%M).log'" && \
tmux new-session -d -s dmon \
  "dcgmi dmon -e 1001,1002,150,155,140,203,204 -d 5000 \
   | tee ~/mnubergemm-logs/dmon-$(date +%Y%m%d-%H%M).log" && \
sleep 5 && tmux ls && ls -lah ~/mnubergemm-logs/burn-72h-*.log
```

Then continue to [§4 Operate](#4-operate-the-running-burn).

---

## 3. Docker path

### 3.1 Pull

```bash
docker pull nvcr.io/0948245400141054/mnubergemm:tensorrt-25.12-v1.13-x86
docker images | grep mnubergemm
```

### 3.2 Smoke test (60 s)

**Terminal A — run the test:**

```bash
docker run --rm --gpus all --ipc=host \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=16g \
  -v $HOME/mnubergemm-logs:/logs -w /opt/mnubergemm \
  nvcr.io/0948245400141054/mnubergemm:tensorrt-25.12-v1.13-x86 \
  bash -c '
    unset CUDA_VISIBLE_DEVICES
    export NCCL_DEBUG=WARN NCCL_P2P_LEVEL=NVL NCCL_IB_DISABLE=1 NCCL_NVLS_ENABLE=0
    mpirun -np 8 --allow-run-as-root --bind-to none --map-by slot \
      --output-filename /logs/ranks-test \
      ./mnubergemm --time_to_run 60 --dynamic_adj \
        --MM_max_workload 65536 --max_workload 65536 \
        --workload GN --duty 0.9 \
        --MM_sm_count 112 --NET_sm_count 32 \
    2>&1 | tail -20
  '
```

**Terminal B — watch GPUs ramp:**

```bash
watch -n 2 'nvidia-smi --query-gpu=index,utilization.gpu,power.draw,temperature.gpu --format=csv'
```

Pass criteria are the same as the enroot path.

### 3.3 Launch the 72-hour burn

```bash
tmux new-session -d -s mnubergemm "docker run --rm \
  --name mnubergemm-burn --gpus all --ipc=host \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=16g \
  -v $HOME/mnubergemm-logs:/logs -w /opt/mnubergemm \
  nvcr.io/0948245400141054/mnubergemm:tensorrt-25.12-v1.13-x86 \
  bash -c 'unset CUDA_VISIBLE_DEVICES && \
   export NCCL_DEBUG=WARN NCCL_P2P_LEVEL=NVL NCCL_CUMEM_ENABLE=1 \
          NCCL_CUMEM_HOST_ENABLE=0 NCCL_IB_DISABLE=1 NCCL_MIN_CTAS=64 \
          NCCL_NVLS_ENABLE=0 && \
   mpirun -np 8 --allow-run-as-root --bind-to none --map-by slot \
     --output-filename /logs/ranks-72h \
     ./mnubergemm --dynamic_adj \
       --MM_max_workload 65536 --max_workload 65536 \
       --time_to_run 259200 --workload GN --duty 0.9 \
       --MM_sm_count 112 --NET_sm_count 32 \
   2>&1 | tee /logs/burn-72h-\$(date +%Y%m%d-%H%M).log'" && \
tmux new-session -d -s dmon \
  "dcgmi dmon -e 1001,1002,150,155,140,203,204 -d 5000 \
   | tee ~/mnubergemm-logs/dmon-$(date +%Y%m%d-%H%M).log" && \
sleep 5 && tmux ls && ls -lah ~/mnubergemm-logs/burn-72h-*.log
```

---

## 4. Operate the running burn

### 4.1 Sanity-check at T+2 min

```bash
grep -E "QUAL_OK|XID|FAILED|QUAL_RUNTIME|GLOBAL PERF|RANK PERF" \
  ~/mnubergemm-logs/burn-72h-*.log | tail -20

# enroot:
tmux ls
# docker:
docker ps | grep mnubergemm
```

- **Pass** — streaming `T:G` and `T:N` pulse lines, no `FAILED` /
  `terminate called` / `QUAL_RUNTIME_ERROR`. Detach SSH; burn rides the
  weekend.
- **Fail** — capture log tail, stop the burn (see §4.3), escalate.

### 4.2 Watch progress (second terminal)

```bash
watch -n 2 'nvidia-smi --query-gpu=index,utilization.gpu,power.draw,temperature.gpu --format=csv \
  && echo "--- burn log tail ---" \
  && tail -3 ~/mnubergemm-logs/burn-72h-*.log'
```

### 4.3 tmux + container controls

| Action | Command |
| --- | --- |
| Attach to burn | `tmux attach -t mnubergemm` |
| Attach to telemetry | `tmux attach -t dmon` |
| Detach from session | `Ctrl-b` then `d` |
| List sessions | `tmux ls` |
| Stop burn (enroot) | `tmux kill-session -t mnubergemm` |
| Stop burn (docker) | `docker stop mnubergemm-burn && tmux kill-session -t mnubergemm` |
| Stop telemetry | `tmux kill-session -t dmon` |

---

## 5. Post-burn analysis

### 5.1 Did the burn complete cleanly?

```bash
LOG=$(ls -t ~/mnubergemm-logs/burn-72h-*.log | head -1)
echo "Log: $LOG"

tail -100 "$LOG"
grep -cE "QUAL_OK|FAILED|abort|QUAL_RUNTIME" "$LOG"

# Xid events from host kernel ring buffer
dmesg -T | grep -iE "xid|nvrm" | tail -50

# Final performance numbers
grep -E "GLOBAL PERF|RANK PERF" "$LOG" | tail -20
```

### 5.2 Telemetry summary

```bash
DMON=$(ls -t ~/mnubergemm-logs/dmon-*.log | head -1)

awk 'NR>2 && $5 ~ /^[0-9.]+$/ {print $5}' "$DMON" \
  | sort -n | awk 'NR==1{min=$1} {max=$1} END{print "Power min/max:", min, "/", max, "W"}'

awk 'NR>2 && $7 ~ /^[0-9.]+$/ {print $7}' "$DMON" \
  | sort -n | awk 'NR==1{min=$1} {max=$1} END{print "Temp min/max:", min, "/", max, "C"}'
```

### 5.3 Cleanup

```bash
tmux kill-session -t mnubergemm 2>/dev/null
tmux kill-session -t dmon 2>/dev/null

# enroot:
enroot remove -f mnubergemm

# docker (image and credentials persist):
docker stop mnubergemm-burn 2>/dev/null
# optional: docker rmi nvcr.io/0948245400141054/mnubergemm:tensorrt-25.12-v1.13-x86

# Rotate NGC key at ngc.nvidia.com → Service Keys
```

---

## 6. Known reference numbers

From a passing 60s smoke test on a healthy 8x B300 node:

| Metric | Expected |
| --- | --- |
| Per-GPU peak power | ~1000–1080 W |
| Per-GPU temperature (steady-state) | 60–75 °C |
| Aggregate GEMM (8 ranks) | ~1.15–1.25 PFlops |
| Aggregate NCCL bandwidth | ~190 GB/s |
| Xid count | 0 |

Significant deviation in any of these on a freshly-provisioned node is a
signal worth investigating before committing to a 72 h burn.

---

## 7. Backlog / future improvements

- **Upgrade host driver to ≥581 (CUDA 13.2 support)** to enable the full
  `GNC` workload, which adds Copy Engine / DMA-path thermal coverage.
- **Pre-stage an NGC service key scoped to org `0948245400141054`** on
  every NVIS-OVA lab box. Keep the key in vault, rotated quarterly.
- **Add the 60s smoke test as a required step in the cluster bring-up SOP.**
  90 seconds catches driver/container mismatches before a customer-visible
  weekend burn.
- **Mirror mnubergemm images to an org accessible to all NVIS-OVA
  accounts** so single-org membership is not a critical-path dependency for
  cluster qualification.

---

*First compiled May 2026 from single-node B300 viking lab validation
(b300-1 through b300-4). Workload config derived from Jeffrey Miller's Eli
Lilly LillyPod sbatch script, adapted to single-node enroot/docker (no
Slurm) and `GN` workload (Copy Engine disabled).*
