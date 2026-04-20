# AI Factory Testing Plan

Tests run in execution order: initial system checks through full-scale workload validation. Automated tests trigger without manual intervention; intermediate diagnostics interrupt burn-in to surface issues early.

---

## Test Execution Order

| # | Test Name | Purpose | Duration |
|---|-----------|---------|----------|
| 1 | **Pre-Flight Checks** | Verify hardware inventory, firmware/driver versions, NVLink/NVSwitch topology, IB fabric health, power/cooling baselines, and BIOS/OS config. Blocks all downstream tests on failure. | < 1 min |
| 2 | **MNUberGEMM Burn-In** *(Automated)* | Stress-test all GPUs via max-intensity GEMM to expose thermal instability, memory errors, power delivery issues, and infant-mortality faults. Downstream tests run within this window. | 24–72 hrs |
| 3 | **Intermediate NCCL Tests** *(During Burn-In)* | AllReduce/AllToAll on partial node subsets as nodes clear burn-in checkpoints. Validates inter-node comms incrementally and surfaces network issues before full-scale tests. | ~5 min/subset |
| 4 | **NCCL AllReduce / AllToAll — Single Node, NVLink** *(Automated)* | Validate intra-node GPU collective bandwidth/latency over NVLink/NVSwitch. Establishes per-node NVLink baseline. | < 5 min |
| 5 | **NCCL AllReduce / AllToAll — Single Node, No NVLink** *(Automated)* | Validate intra-node GPU collectives over PCIe only. Confirms PCIe integrity; regression reference for nodes where NVLink is unavailable or degraded. | < 5 min |
| 6 | **NCCL AllReduce / AllToAll — Rack** | Validate collectives across all nodes in a rack. Exercises ToR switch paths and RDMA fabric cabling under all-to-all traffic. | ~5 min |
| 7 | **NCCL AllReduce / AllToAll — Scalable Unit (SU)** | Validate inter-node bandwidth/latency across all nodes in a single SU over RDMA. Identifies rail misconfigs, bad cables, or underperforming HCAs. | ~5 min |
| 8 | **NCCL AllReduce / AllToAll — Across SUs** | Validate collectives spanning multiple SUs. Exercises spine switching, inter-SU cabling, and routing tables. | ~5 min |
| 9 | **NCCL AllReduce / AllToAll — All Handover Hosts** | Full-fabric collective test across all handover nodes. Confirms end-to-end network health and bisection bandwidth at production scale. Must pass before model-level tests. | ~5 min |
| 10 | **Llama 3.1 403B Pre-Training — All Handover Hosts** | End-to-end pre-training across all handover nodes. Validates target MFU with no loss spikes, checkpoint corruption, or node dropouts. | ~45 min |
| 11 | **Nemotron 3 — All Handover Hosts** | Nemotron 3 workload across all handover nodes. Second independent signal of system health; validates NVIDIA-specific kernels and training stack. | ~1 hr |

---

## Pass / Fail Criteria

| Test | Hard Block on Failure |
|------|-----------------------|
| Pre-Flight Checks | Yes — no downstream tests run |
| MNUberGEMM Burn-In | Yes — failed nodes quarantined |
| Intermediate NCCL Tests | Yes — failed nodes pulled before full-scale NCCL |
| NCCL Single-Node (NVLink / No NVLink) | Yes — per node |
| NCCL SU / Rack / Across SUs | Yes |
| NCCL All Handover Hosts | Yes — blocks model-level tests |
| Llama 3.1 403B Pre-Training | Yes — blocks handover |
| Nemotron 3 | Yes — blocks handover |

---

## Notes

- Tests marked *(Automated)* trigger programmatically on prerequisite completion.
- Intermediate diagnostics (#3) and single-node NCCL tests (#4, #5) run concurrently across different nodes while burn-in continues.
- Nodes failing burn-in or single-node NCCL are removed from the handover pool and re-queued for hardware investigation.
- Duration estimates vary with cluster size, message sizes, and iteration counts configured per site.
