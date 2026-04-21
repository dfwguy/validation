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

## Time to Market (TTM) — Reduced Scope Handovers

When handing over a **single node** or a **rack** (rather than a full scalable unit), multi-node tests that require fabric or cross-node topology are removed. The table below shows which tests survive each scope reduction. Tests marked **Removed** are dropped entirely; tests marked **Scoped** run but only against the nodes being handed over.

| # | Test Name | Tier | Single Node | Rack |
|---|-----------|------|-------------|------|
| 1 | Pre-Flight Checks | SNT1 | Included | Included |
| 2 | DCGM Diagnostics (`dcgmi -r 3`) | SNT2 | Included | Included |
| 3 | NCCL Single-Node — NVLink | SNT2 | Included | Included |
| 4 | NCCL Single-Node — No NVLink | SNT2 | Included | Included |
| 5 | MNUberGEMM Burn-In | SNT3 | Included | Included |
| 6 | Intermediate NCCL + Workload Tests | — | **Removed** — no peer nodes for inter-node collectives or distributed workload | Scoped to rack nodes |
| 7 | Network Fabric Health Check | MNT1 | **Removed** — no fabric to validate | Included |
| 8 | NCCL AllReduce / AllToAll — Rack | MNT2 | **Removed** | Included |
| 9 | NCCL AllReduce / AllToAll — Scalable Unit | MNT2 | **Removed** | **Removed** — no full SU |
| 10 | NCCL AllReduce / AllToAll — Across SUs | MNT2 | **Removed** | **Removed** — single rack only |
| 11 | NCCL AllReduce / AllToAll — All Handover Hosts | MNT2 | **Removed** | Scoped to rack |
| 12 | Llama 3.1 403B Pre-Training | MNT3 | **Removed** | **Removed** — workload requires multi-rack scale |
| 13 | Nemotron 3 | MNT3 | **Removed** | **Removed** — workload requires multi-rack scale |

### TTM Coverage Summary

| Scope | Tests Run | Tests Removed |
|-------|-----------|---------------|
| Single Node | SNT1–SNT3 (tests 1–5) | Tests 6–13 |
| Rack | SNT1–SNT3 + MNT1–MNT2 (tests 1–8, 11 scoped) | Tests 9, 10, 12, 13 |
| Sweet Spot / Hybrid | All tests | — |

> **What this means at handover:** A single-node TTM handover confirms the node is individually healthy but provides no signal on fabric, inter-node bandwidth, or distributed workload behavior. A rack TTM handover validates intra-rack fabric and collective performance but cannot confirm SU-level routing, cross-SU paths, or production-scale model training throughput. Customers receiving TTM handovers should expect remaining MNT-tier validation to complete before full production load is placed on the system.
