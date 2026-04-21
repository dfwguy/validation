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

## Time to Market — Single Node (8-Way)

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

## Time to Market — Rack (NVL72)

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

---

## Tools for Exhaustive Testing of All Components

| Tool | Source | Category | What It Tests |
|------|--------|----------|---------------|
| **stress-ng** | `apt install stress-ng` / [github.com/ColinIanKing/stress-ng](https://github.com/ColinIanKing/stress-ng) | CPU / memory / I/O stress | General-purpose system stressor. Exercises CPU (arithmetic, bit-ops, SIMD), memory subsystem (mmap, vm, cache), I/O, and OS primitives via hundreds of configurable stressors. Used to expose thermal instability, power-delivery limits, and hardware faults on compute nodes before GPU-level burn-in. |
| **STREAM** | [cs.virginia.edu/stream](https://www.cs.virginia.edu/stream/) | Memory bandwidth | The industry-standard benchmark for sustained CPU memory bandwidth. Measures Copy, Scale, Add, and Triad throughputs (GB/s) against system-memory arrays too large to fit in cache. Validates DRAM channels and NUMA configuration on CPU nodes; used as the memory-bandwidth baseline before GPU workloads. |
| **stressapptest** | [github.com/stressapptest/stressapptest](https://github.com/stressapptest/stressapptest) | Memory integrity | Google's memory and I/O stress test. Randomizes memory access patterns across all DRAM while simultaneously stressing I/O and network paths. Designed to find marginal DRAM cells, ECC-uncorrectable errors, and signal-integrity faults that lighter tests miss. Used for extended CPU-node memory validation. |
| **fio** | `apt install fio` / [github.com/axboe/fio](https://github.com/axboe/fio) | Storage I/O | Flexible I/O tester for block and file storage. Configures arbitrary mixes of sequential/random reads and writes at any queue depth, block size, and thread count. Measures throughput (MB/s), IOPS, and latency (µs p50/p99/p999). Used to validate local NVMe drives and shared storage mounts (e.g., VAST, Lustre, WekaFS) against expected performance targets. |
| **ethr** | [github.com/microsoft/ethr](https://github.com/microsoft/ethr) | Network throughput & latency | TCP/UDP/ICMP network performance tool for in-band and storage network validation. Measures bandwidth, packets-per-second, and round-trip latency between node pairs. Used to verify in-band management network links and storage fabric NICs (ConnectX / BlueField) before and after GPU-level networking tests. Complements NCCL tests by isolating CPU-side network performance from GPU-to-GPU collective performance. |
| **perftest** | `apt install perftest` / [github.com/linux-rdma/perftest](https://github.com/linux-rdma/perftest) | RDMA / InfiniBand per-link | Suite of RDMA micro-benchmarks (`ib_write_bw`, `ib_read_bw`, `ib_send_bw`, `ib_write_lat`, `ib_read_lat`) that measure bandwidth and latency on individual InfiniBand ports between a pair of nodes. Unlike NCCL, which aggregates across all links simultaneously, perftest isolates a single port pair — making it the right tool for identifying a degraded transceiver, a bad cable, or a misconfigured HCA before collective tests obscure the fault behind aggregate numbers. |
| **nvbandwidth** | [github.com/NVIDIA/nvbandwidth](https://github.com/NVIDIA/nvbandwidth) | GPU memory & PCIe bandwidth | NVIDIA's dedicated bandwidth measurement tool. Quantifies HBM bandwidth per GPU (device-to-device within a node), host-to-device and device-to-host PCIe transfer rates, and NVLink/NVSwitch peer bandwidth. Surfaces regressions that DCGM and MNUberGEMM do not report as explicit bandwidth numbers — in particular, PCIe width or speed negotiation faults (e.g., a GPU training at x8 instead of x16) and HBM channel failures that reduce available memory bandwidth below spec. |

---

## Reference

- [NVIS AI Factory Delivery Methodology](clustermods-methodology/output/NVIS69-DG11849001-NVIS-AI-Factory-Delivery-Methodology-Refactored-2026-03-30.md#52-cluster-validation-test-tiers) — test tiers SNT1–SNT3 and MNT1–MNT3, delivery methodologies (Hybrid, Exhaustive, Time To Market), and grouping rules
- [ClusterMODS MOP](cmods-docs/MOP/CMODS-MOP-NEW.md) — ClusterMODS installation, configuration, test plan execution, and node management
- [NVIS HPC SA Repository](hpc-row-scripts/) — scripts and documentation for provisioning and validating SuperPOD clusters: firmware, network, storage, BCM, and validation tooling
- [GB200 NVL72 Validation MOP](validation-mops/GB200_MOP.md) — three-phase validation procedure for GB200 clusters
- [GB300 / B300 Validation MOP](validation-mops/GB300_B300_Validation_MOP.md) — three-phase validation procedure for GB300 and B300 clusters
- [Cable Validation Tool (CVT) MOP](validation-mops/Cable-Validation-Tool-MOP.md) — deploying and running CVT to validate Layer 1 cabling against a golden P2P topology file (referenced in test #7)
- [ClusterMinder MOP](validation-mops/ClusterMinder-MOP.md) — deploying ClusterMinder for cluster-wide power, temperature, and health telemetry via Redfish BMC
- [NVIS Observability Suite](nvis-observability/README.md) — GPU health (DCGM), network fabric dashboards, Slurm job telemetry, and log correlation; primary tool for fabric monitoring in test #7 and ongoing observability through handover
- [Meta CSP NCCL Tests](meta-csp-nccl-tests/Meta_CSP_NCCL_Tests.md) — NCCL test procedures and configurations used for CSP-scale validation
- [NVIS Exemplar MOP](nvis-exemplar/Exemplar_MOP.md) — reference MOP for NVIS exemplar cluster validation and delivery
- [LLM Benchmarking Collection (Internal)](llm-benchmarking-collection-internal/exemplar.yaml) — source of the Exemplar workload definition; `exemplar.yaml` defines the LLM training benchmark configuration used in Exemplar runs (branch: `perf/26.02`)

---

## To-Do / To Reconcile

### High Priority

- **"Time to Market" naming collision** — The two TTM sections (Single Node, Rack) include MNUberGEMM Burn-In (SNT3), which the [NVIS AI Factory Delivery Methodology](clustermods-methodology/output/NVIS69-DG11849001-NVIS-AI-Factory-Delivery-Methodology-Refactored-2026-03-30.md) explicitly defines as Hybrid content, not TTM. The methodology's TTM runs only the shared baseline (inventory + minimum viable fabric + representative workload) with no burn-in or extra campaigns. What these sections actually describe is **Hybrid methodology scoped to a smaller delivery increment** (single node or single rack). Options: rename the sections to "Hybrid — Single Node" and "Hybrid — Rack," or add an explicit callout that these scenarios apply Hybrid methodology depth at a partial-delivery granularity.

- **Hybrid section omits Path B → Exhaustive bifurcation** — The methodology defines Hybrid as a bifurcation: Path A (passing nodes) goes to production; Path B (failing nodes/scope) enters full Exhaustive validation (SNT1 → SNT2 → SNT3 → MNT as required). The pass/fail table captures the gating logic but does not describe what happens to failed scope. Add a note or row clarifying that quarantined nodes follow the Exhaustive path per the methodology.

### Medium Priority

- **DCGM diagnostic level mismatch** — This plan specifies `dcgmi -r 3` (Level 3, ~20 min) in test #2. Both the [GB200 MOP](validation-mops/GB200_MOP.md) and [GB300/B300 MOP](validation-mops/GB300_B300_Validation_MOP.md) use `dcgmi diag -r 2` (Level 2). Decide which level is correct for this plan and align the MOPs or document the rationale for running Level 3 here.

### Low Priority

- **Workload naming: "Nemotron 3" vs "Nemotron-4"** — Test #13 lists "Nemotron 3" but the [GB200 MOP](validation-mops/GB200_MOP.md) uses Nemotron-4 (15B, via `llmb-run`), and the [GB300/B300 MOP](validation-mops/GB300_B300_Validation_MOP.md) uses DeepSeek-V3 671B FP8 as the Phase 1 workload. Confirm whether test #13 should reference Nemotron-4 (or a platform-appropriate equivalent) and update accordingly.

