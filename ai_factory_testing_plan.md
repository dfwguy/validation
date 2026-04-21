# AI Factory Testing Plan

Tests run in execution order: initial system checks through full-scale workload validation. Automated tests trigger without manual intervention.

---

## Test Execution Order — Sweet Spot / Hybrid

| # | Test Name | Purpose | Duration | Test Tier |
|---|-----------|---------|----------|-----------|
| 1 | **Pre-Flight Checks** | Verify hardware inventory, firmware/driver versions, NVLink/NVSwitch topology, IB fabric health, power/cooling baselines, and BIOS/OS config. Blocks all downstream tests on failure. | < 1 min | SNT1 |
| 2 | **DCGM Diagnostics (`dcgmi -r 3`)** *(Automated)* | Run level-3 DCGM diagnostics on all nodes. Validates GPU memory, compute, and interconnect health per node before committing to long burn-in. Quarantines failing nodes early. | ~20 min | SNT2 |
| 3 | **NCCL AllReduce / AllToAll — Single Node, NVLink** *(Automated)* | Validate intra-node GPU collective bandwidth/latency over NVLink/NVSwitch. Establishes per-node NVLink baseline. | < 5 min | SNT2 |
| 4 | **NCCL AllReduce / AllToAll — Single Node, No NVLink** *(Automated)* | Validate intra-node GPU collectives over PCIe only. Confirms PCIe integrity; regression reference for nodes where NVLink is unavailable or degraded. | < 5 min | SNT2 |
| 5 | **MNUberGEMM Burn-In** *(Automated)* | Stress-test all GPUs via max-intensity GEMM to expose thermal instability, memory errors, power delivery issues, and infant-mortality faults. | 24–72 hrs | SNT3 |
| 6 | **Intermediate NCCL + Workload Tests** *(During Burn-In)* | MNUberGEMM is paused at burn-in checkpoints to run AllReduce/AllToAll on partial node subsets and a small-scale workload (reduced-iteration pre-training) on a node subset. Provides early signal on inter-node network functionality and confirms containers are healthy and workloads behave as expected before full-scale tests. | ~20 min/subset | — |
| 7 | **Network Fabric Health Check** | Confirm network dashboard is green and CVT (or equivalent fabric validation tool) reports no errors. Validates fabric inventory, topology, and link health across the full scope before performance testing begins. | ~15 min | MNT1 |
| 8 | **NCCL AllReduce / AllToAll — Rack** | Validate collectives across all nodes in a rack. Exercises ToR switch paths and RDMA fabric cabling under all-to-all traffic. | ~5 min | MNT2 |
| 9 | **NCCL AllReduce / AllToAll — Scalable Unit (SU)** | Validate inter-node bandwidth/latency across all nodes in a single SU over RDMA. Identifies rail misconfigs, bad cables, or underperforming HCAs. | ~5 min | MNT2 |
| 10 | **NCCL AllReduce / AllToAll — Across SUs** | Validate collectives spanning multiple SUs. Exercises spine switching, inter-SU cabling, and routing tables. | ~5 min | MNT2 |
| 11 | **NCCL AllReduce / AllToAll — All Handover Hosts** | Full-fabric collective test across all handover nodes. Confirms end-to-end network health and bisection bandwidth at production scale. Must pass before model-level tests. | ~5 min | MNT2 |
| 12 | **Llama 3.1 403B Pre-Training — All Handover Hosts** | End-to-end pre-training across all handover nodes. Validates target MFU with no loss spikes, checkpoint corruption, or node dropouts. | ~45 min | MNT3 |
| 13 | **Nemotron 3 — All Handover Hosts** | Nemotron 3 workload across all handover nodes. Second independent signal of system health; validates NVIDIA-specific kernels and training stack. | ~1 hr | MNT3 |
| — | **Remediation — Failed Nodes / Components** | Hardware investigation, repair, and re-validation for any nodes quarantined during testing. Includes fault isolation, component replacement, and re-running affected tests. Duration scales with failure count, component availability, and cluster size. | 3+ days (scale-dependent) | — |
| — | **New Product Tuning** | System-level tuning required on new hardware platforms — BIOS settings, fabric configs, driver parameters, and performance baseline calibration. Must be completed before or alongside burn-in on first-generation deployments. | 3+ days | — |

---

## Pass / Fail Criteria

| Test | Hard Block on Failure |
|------|-----------------------|
| Pre-Flight Checks | Yes — no downstream tests run |
| DCGM Diagnostics (`dcgmi -r 3`) | Yes — failed nodes quarantined before burn-in |
| NCCL Single-Node (NVLink / No NVLink) | Yes — per node |
| MNUberGEMM Burn-In | Yes — failed nodes quarantined |
| Intermediate NCCL + Workload Tests | Yes — failed nodes pulled; container issues fixed |
| Network Fabric Health Check | Yes — dashboard errors or CVT failures block performance testing |
| NCCL SU / Rack / Across SUs | Yes |
| NCCL All Handover Hosts | Yes — blocks model-level tests |
| Llama 3.1 403B Pre-Training | Yes — blocks handover |
| Nemotron 3 | Yes — blocks handover |

---

## Notes

- Tests marked *(Automated)* trigger programmatically on prerequisite completion.
- Intermediate NCCL tests (#6) pause MNUberGEMM at burn-in checkpoints; burn-in resumes after each subset completes.
- Network Fabric Health Check (#7) must show a clean dashboard and passing CVT (or equivalent) before rack-level NCCL tests begin.
- Nodes failing single-node NCCL, burn-in, or intermediate NCCL are removed from the handover pool and re-queued for hardware investigation.
- Duration estimates vary with cluster size, message sizes, and iteration counts configured per site.

---

## TTM — Single Node (8-Way)

Handing over individual 8-way nodes. No peer nodes available, so all inter-node and multi-node tests are removed.

| # | Test Name | Tier | Status |
|---|-----------|------|--------|
| 1 | Pre-Flight Checks | SNT1 | Included |
| 2 | DCGM Diagnostics (`dcgmi -r 3`) | SNT2 | Included |
| 3 | NCCL Single-Node — NVLink | SNT2 | Included |
| 4 | NCCL Single-Node — No NVLink | SNT2 | Included |
| 5 | MNUberGEMM Burn-In | SNT3 | Included |
| 6 | Intermediate NCCL + Workload Tests | — | **Removed** — inter-node collectives and distributed workload require peer nodes |
| 7 | Network Fabric Health Check | MNT1 | Included — validates fabric port and link health for the node |
| 8 | NCCL AllReduce / AllToAll — Rack | MNT2 | **Removed** — no peer nodes |
| 9 | NCCL AllReduce / AllToAll — Scalable Unit | MNT2 | **Removed** — no peer nodes |
| 10 | NCCL AllReduce / AllToAll — Across SUs | MNT2 | **Removed** — no peer nodes |
| 11 | NCCL AllReduce / AllToAll — All Handover Hosts | MNT2 | **Removed** — redundant with single-node NCCL |
| 12 | Llama 3.1 403B Pre-Training | MNT3 | **Removed** — requires multi-node distributed training |
| 13 | Nemotron 3 | MNT3 | **Removed** — requires multi-node distributed training |

---

## TTM — Rack (NVL72)

Handing over a single NVL72 rack. Intra-rack tests and workloads run at rack scope. Tests that require SU-level topology or span the full deployment are removed.

| # | Test Name | Tier | Status |
|---|-----------|------|--------|
| 1 | Pre-Flight Checks | SNT1 | Included |
| 2 | DCGM Diagnostics (`dcgmi -r 3`) | SNT2 | Included |
| 3 | NCCL Single-Node — NVLink | SNT2 | Included |
| 4 | NCCL Single-Node — No NVLink | SNT2 | Included |
| 5 | MNUberGEMM Burn-In | SNT3 | Included |
| 6 | Intermediate NCCL + Workload Tests | — | Included — scoped to rack nodes |
| 7 | Network Fabric Health Check | MNT1 | Included |
| 8 | NCCL AllReduce / AllToAll — Rack | MNT2 | Included |
| 9 | NCCL AllReduce / AllToAll — Scalable Unit | MNT2 | **Removed** — single rack; no SU-level topology |
| 10 | NCCL AllReduce / AllToAll — Across SUs | MNT2 | **Removed** — no cross-SU paths in a single rack |
| 11 | NCCL AllReduce / AllToAll — All Handover Hosts | MNT2 | **Removed** — spans all nodes in the full deployment, not just this rack |
| 12 | Llama 3.1 403B Pre-Training | MNT3 | Included — scoped to NVL72 rack |
| 13 | Nemotron 3 | MNT3 | Included — scoped to NVL72 rack |
