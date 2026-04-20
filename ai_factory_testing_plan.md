# AI Factory Testing Plan

Tests run in execution order: initial system checks through full-scale workload validation. Automated tests trigger without manual intervention.

---

## Test Execution Order

| # | Test Name | Purpose | Duration |
|---|-----------|---------|----------|
| 1 | **Pre-Flight Checks** | Verify hardware inventory, firmware/driver versions, NVLink/NVSwitch topology, IB fabric health, power/cooling baselines, and BIOS/OS config. Blocks all downstream tests on failure. | < 1 min |
| 2 | **DCGM Diagnostics (`dcgmi -r 3`)** *(Automated)* | Run level-3 DCGM diagnostics on all nodes. Validates GPU memory, compute, and interconnect health per node before committing to long burn-in. Quarantines failing nodes early. | ~20 min |
| 3 | **NCCL AllReduce / AllToAll — Single Node, NVLink** *(Automated)* | Validate intra-node GPU collective bandwidth/latency over NVLink/NVSwitch. Establishes per-node NVLink baseline. | < 5 min |
| 4 | **NCCL AllReduce / AllToAll — Single Node, No NVLink** *(Automated)* | Validate intra-node GPU collectives over PCIe only. Confirms PCIe integrity; regression reference for nodes where NVLink is unavailable or degraded. | < 5 min |
| 5 | **MNUberGEMM Burn-In** *(Automated)* | Stress-test all GPUs via max-intensity GEMM to expose thermal instability, memory errors, power delivery issues, and infant-mortality faults. | 24–72 hrs |
| 6 | **Intermediate NCCL Tests** *(During Burn-In)* | MNUberGEMM is paused to run AllReduce/AllToAll on partial node subsets at burn-in checkpoints. Provides early signal on inter-node functionality and surfaces network issues before full-scale tests. | ~5 min/subset |
| 7 | **NCCL AllReduce / AllToAll — Rack** | Validate collectives across all nodes in a rack. Exercises ToR switch paths and RDMA fabric cabling under all-to-all traffic. | ~5 min |
| 8 | **NCCL AllReduce / AllToAll — Scalable Unit (SU)** | Validate inter-node bandwidth/latency across all nodes in a single SU over RDMA. Identifies rail misconfigs, bad cables, or underperforming HCAs. | ~5 min |
| 9 | **NCCL AllReduce / AllToAll — Across SUs** | Validate collectives spanning multiple SUs. Exercises spine switching, inter-SU cabling, and routing tables. | ~5 min |
| 10 | **NCCL AllReduce / AllToAll — All Handover Hosts** | Full-fabric collective test across all handover nodes. Confirms end-to-end network health and bisection bandwidth at production scale. Must pass before model-level tests. | ~5 min |
| 11 | **Llama 3.1 403B Pre-Training — All Handover Hosts** | End-to-end pre-training across all handover nodes. Validates target MFU with no loss spikes, checkpoint corruption, or node dropouts. | ~45 min |
| 12 | **Nemotron 3 — All Handover Hosts** | Nemotron 3 workload across all handover nodes. Second independent signal of system health; validates NVIDIA-specific kernels and training stack. | ~1 hr |

---

## Pass / Fail Criteria

| Test | Hard Block on Failure |
|------|-----------------------|
| Pre-Flight Checks | Yes — no downstream tests run |
| DCGM Diagnostics (`dcgmi -r 3`) | Yes — failed nodes quarantined before burn-in |
| NCCL Single-Node (NVLink / No NVLink) | Yes — per node |
| MNUberGEMM Burn-In | Yes — failed nodes quarantined |
| Intermediate NCCL Tests | Yes — failed nodes pulled before full-scale NCCL |
| NCCL SU / Rack / Across SUs | Yes |
| NCCL All Handover Hosts | Yes — blocks model-level tests |
| Llama 3.1 403B Pre-Training | Yes — blocks handover |
| Nemotron 3 | Yes — blocks handover |

---

## Notes

- Tests marked *(Automated)* trigger programmatically on prerequisite completion.
- Intermediate NCCL tests (#6) pause MNUberGEMM at burn-in checkpoints; burn-in resumes after each subset completes.
- Nodes failing single-node NCCL, burn-in, or intermediate NCCL are removed from the handover pool and re-queued for hardware investigation.
- Duration estimates vary with cluster size, message sizes, and iteration counts configured per site.
