# AI Factory Testing Plan

## Overview

This document outlines the testing plan for AI factory validation and handover. Tests are organized in execution order, from initial system checks through full-scale workload validation. Automated tests are triggered without manual intervention; intermediate diagnostic tests interrupt burn-in to surface issues early.

---

## Test Execution Order

| # | Test Name | Purpose | Estimated Duration |
|---|-----------|---------|-------------------|
| 1 | **Pre-Flight Checks** | Verify hardware inventory, firmware versions, driver versions, NVLink/NVSwitch topology, InfiniBand fabric health, power and cooling baselines, BIOS/UEFI settings, and OS configuration before any workload is run. Blocks all downstream tests if failures are detected. | < 1 minute |
| 2 | **MNUberGEMM Burn-In** *(Automated)* | Stress-test all GPUs on a host using maximum-intensity GEMM operations to expose thermal instability, memory errors, power delivery issues, and infant-mortality hardware faults. Runs continuously in the background; downstream tests draw on this window. Automatically triggered post-pre-flight. | 24–72 hours continuous |
| 3 | **Intermediate NCCL Tests** *(During Burn-In)* | Run NCCL AllReduce / AllToAll tests on partial node subsets (e.g., partial SU or partial rack) as nodes complete burn-in checkpoints, before the full node pool is available. Validates inter-node collective communication health incrementally, surfaces network misconfigurations or underperforming links early, and reduces risk of failures in the full-scale NCCL tests downstream. | ~5 minutes per subset |
| 4 | **NCCL AllReduce / AllToAll — Single Node, NVLink** *(Automated)* | Validate intra-node GPU collective communication bandwidth and latency over NVLink / NVSwitch fabric. Establishes per-node NVLink performance baseline. Automatically triggered once a node passes burn-in checkpoint. | < 5 minutes |
| 5 | **NCCL AllReduce / AllToAll — Single Node, No NVLink** *(Automated)* | Validate intra-node GPU collective communication over PCIe only (NVLink disabled / absent). Confirms PCIe fabric integrity and serves as a regression reference for nodes where NVLink is unavailable or degraded. Automatically triggered alongside test #4. | < 5 minutes |
| 6 | **NCCL AllReduce / AllToAll — Rack** | Validate collective communication across all nodes within a single rack. Exercises top-of-rack switch paths and verifies rack-level InfiniBand cabling and port health under all-to-all traffic patterns. | ~5 minutes |
| 7 | **NCCL AllReduce / AllToAll — Scalable Unit (SU)** | Validate inter-node collective communication bandwidth and latency across all nodes within a single Scalable Unit using InfiniBand. Identifies rail misconfigurations, bad cables, or underperforming HCAs within the SU boundary. | ~5 minutes |
| 8 | **NCCL AllReduce / AllToAll — Across SUs** | Validate collective communication spanning multiple Scalable Units. Exercises spine-layer switching, inter-SU cabling, and routing tables. Identifies bandwidth bottlenecks or asymmetric paths at the SU interconnect layer. | ~5 minutes |
| 9 | **NCCL AllReduce / AllToAll — All Handover Hosts** | Full-fabric collective communication test across the complete set of nodes to be handed over to the customer. Confirms end-to-end network health, bisection bandwidth, and collective efficiency at production scale. Must pass before model-level tests are initiated. | ~5 minutes |
| 10 | **Llama 3.1 403B Pre-Training Job — All Handover Hosts** | Run a representative pre-training workload using Llama 3.1 403B across all handover nodes to validate end-to-end system integration: GPU compute, NVLink, InfiniBand, storage I/O, and job scheduling. Confirms the cluster sustains target MFU and does not produce loss spikes, checkpoint corruption, or node dropouts under a realistic LLM training regime. | ~45 minutes |
| 11 | **Nemotron 3 — All Handover Hosts** | Run a Nemotron 3 workload across all handover nodes to validate NVIDIA-specific model optimizations, custom kernels, and training stack compatibility at scale. Provides a second independent signal of system health distinct from the Llama workload. | ~1 hour depending on customer desire |

---

## Pass / Fail Criteria Summary

| Test | Hard Block on Failure |
|------|-----------------------|
| Pre-Flight Checks | Yes — no downstream tests run |
| MNUberGEMM Burn-In | Yes — nodes with uncorrected errors are quarantined |
| Intermediate NCCL Tests | Yes — nodes failing partial-subset tests are pulled for investigation before full-scale NCCL tests |
| NCCL Single-Node (NVLink / No NVLink) | Yes — per node |
| NCCL SU / Rack / Across SUs | Yes |
| NCCL All Handover Hosts | Yes — blocks model-level tests |
| Llama 3.1 403B Pre-Training | Yes — blocks handover |
| Nemotron 3 | Yes — blocks handover |

---

## Notes

- **Automation:** Tests marked *(Automated)* are triggered programmatically without operator intervention upon successful completion of their prerequisite.
- **Parallelism:** Intermediate diagnostics (#3) and single-node NCCL tests (#4, #5) can run concurrently across different nodes while burn-in continues on others.
- **Quarantine policy:** Any node failing burn-in or NCCL single-node tests is removed from the handover pool and re-queued for hardware investigation before re-integration.
- **Duration estimates** are approximate and vary with cluster size, message sizes swept, and iteration counts configured per site.
