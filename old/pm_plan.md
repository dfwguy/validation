# NVIDIA NOVA TEAM — Program Management Plan
**NVIDIA CONFIDENTIAL • INTERNAL USE ONLY**

**NVIDIA | NVIS Professional Services**

Prepared April 2026 by Shai Kamak
Edits May 2026 by Bryan Reese

---

## Executive Summary

The NOVA team is a cross-functional program within NVIDIA's NVIS Professional Services organization, focused on the Bring-up & Validation of AI Factory clusters built on GB200, GB300, and SuperPOD platforms. The team ensures hardware is sound, the software stack is aligned, and performance meets NVIDIA Reference Architecture standards before cluster handover to customers.

This document provides the NOVA team's Program Management framework, structured around three core PM deliverables:

- **Tasks** — A phased work breakdown covering Readiness, Execution, Validation, and Handover.
- **Risks** — A RAID-aligned risk register with likelihood, impact, early indicators, and mitigations.
- **Action Items** — Near-term, owner-assigned actions to move the program forward immediately.

The framework is grounded in documented NVIS activities, lessons learned from GB200 deployments, and standard NVIS governance practices, including RAG scoring, escalation thresholds, and Wrike-compatible task structures.

| Item | Summary |
|---|---|
| Team | NOVA — NVIS Bring-up & Validation |
| Program Stage | Early Planning |
| Platforms | GB200, GB300, DGX SuperPOD |
| Audience | NOVA Team, Senior Leadership, Cross-functional Partners |
| PM Methodology | Program Management with RAID log, RAG scoring, phase gating, and governance checkpoints |
| Key Risks | Firmware delays, fabric instability at scale, shared cluster access, platform maturity gaps, limited specialist capacity, tooling gaps |

---

## Section 1: Task Register

The NOVA team's work is organized into four phases aligned with the NVIS Bring-up & Validation lifecycle. Each task maps to an owner role and a status to enable live tracking in Wrike or an equivalent PM tool.

### 1.1 Phase Structure

The four phases gate progression. No phase may begin unless the prior phase's exit criteria are met or an explicit PMO exception is approved.

| Phase | Purpose | Gate |
|---|---|---|
| Phase 1: Bring-up Readiness | Confirm all prerequisites before power-on: firmware, access, SMEs, tooling, and escalation paths. | Readiness RAG = Green or approved Amber |
| Phase 2: Bring-up Execution | Hardware power-on, fabric bring-up (NVLink, InfiniBand, UFM), and baseline health verification. | No critical HW/fabric blockers |
| Phase 3: Validation Execution | Formal performance validation: NV Qual, HPL, NCCL, ClusterKIT, long-run burn-in. | All tests pass or exceptions approved |
| Phase 4: Post-Validation & Handover | Validation report, known-issue logging, lessons learned capture, and operational handover. | RAG = Green or approved Amber; handover signed off |

### 1.2 Full Task List

| Task ID | Task Name & Description | Owner Role | Phase | Status |
|---|---|---|---|---|
| **PHASE 1 — BRING-UP READINESS** |||||
| T-01 | Define Bring-up vs Validation vs Production boundaries and obtain customer sign-off on scope delineation. | PM | Phase 1 | Not Started |
| T-02 | Document and lock target firmware baseline across all components (NICs, switches, BIOS, ASIC). Assign upgrade ownership (OEM / Customer / NVIS). | PM / SA | Phase 1 | Not Started |
| T-03 | Validate OS image availability and confirm NCCL, HPL, and diagnostics packages are present and version-matched. | SA | Phase 1 | Not Started |
| T-04 | Negotiate and confirm exclusive validation blackout windows with the customer. Document agreed maintenance schedule. | PM | Phase 1 | Not Started |
| T-05 | Assign Validation SMEs (fabric, firmware, low-level diagnostics) and confirm availability. Flag conflicts to PMO. | PMO / PM | Phase 1 | Not Started |
| T-06 | Confirm remote access, UFM / BCManager availability, and monitoring/telemetry tooling (DCGM, UFM Telemetry, ClusterMinder). | SA | Phase 1 | Not Started |
| T-07 | Confirm escalation path: owners, governance meeting cadence, and SLAs for fabric, firmware, and engineering escalations. | PM | Phase 1 | Not Started |
| T-08 | Complete Bring-up Readiness RAG assessment across all six dimensions. No Execution phase to proceed with any Red rating. | PM | Phase 1 | Not Started |
| **PHASE 2 — BRING-UP EXECUTION** |||||
| T-09 | Coordinate hardware power-on sequence. Execute power-on checklist; validate server and tray power-on health. | HW Team | Phase 2 | Not Started |
| T-10 | Execute NVSwitch and NVLink bring-up. Confirm baseline fabric topology and link health. | SA / Fabric SME | Phase 2 | Not Started |
| T-11 | Execute InfiniBand fabric bring-up: UFM configuration, IBDiagnet, netdiscover, and fabric health checks. | SA / Fabric SME | Phase 2 | Not Started |
| T-12 | Detect and remediate ASIC, BIOS, and firmware mismatches across racks. Log all findings as NVBugs. | SA | Phase 2 | Not Started |
| T-13 | Execute on-site subset of factory validation tests (e.g., L11 sanity checks) if required post-shipment. | Validation SME | Phase 2 | Not Started |
| T-14 | Confirm baseline health verification: no critical hardware or fabric blocking issues present before proceeding to Phase 3. | SA / PM | Phase 2 | Not Started |
| **PHASE 3 — VALIDATION EXECUTION** |||||
| T-15 | Execute NV Qual and NVIDIA Field Diagnostics (GPU FD, HGX FD, IST) as applicable to the platform. | Validation SME | Phase 3 | Not Started |
| T-16 | Execute HPL, NCCL, and ClusterKIT performance and stress tests. Run long-duration burn-in to surface slow-rack and fabric instability. | Validation SME | Phase 3 | Not Started |
| T-17 | Execute GPUburn and fabric topology validation. Verify NVLink recovery behavior under load. | Validation SME | Phase 3 | Not Started |
| T-18 | Identify and document slow racks, NVLink recovery failures, IB link flaps, and BER events. Open NVBugs for all findings. | SA / Validation SME | Phase 3 | Not Started |
| T-19 | Run LLM and stream benchmarks if in scope. Validate against NVIDIA Reference Architecture performance baselines. | Validation SME | Phase 3 | Not Started |
| T-20 | Apply Go / No-Go criteria. Document any deviations with PMO-approved exceptions before proceeding to Phase 4. | PM | Phase 3 | Not Started |
| **PHASE 4 — POST-VALIDATION & HANDOVER** |||||
| T-21 | Compile the formal Validation Report. Include test results, known issues, NVBug references, and configuration baseline. | PM | Phase 4 | Not Started |
| T-22 | Log all known issues with NVBug IDs and RAID entries. Clearly document deviations and approved exceptions. | PM / SA | Phase 4 | Not Started |
| T-23 | Set final Readiness RAG to Green or approved Amber. Obtain PMO sign-off before handover. | PM | Phase 4 | Not Started |
| T-24 | Submit lessons learned to NVIS Knowledge Base (ServiceNow). Tag entries by platform, failure type, and resolution. | PM / SA | Phase 4 | Not Started |
| T-25 | Complete team readout (Tech Huddle or equivalent). Share key findings and improvement recommendations. | PM / Tech Lead | Phase 4 | Not Started |
| T-26 | Confirm monitoring and operational readiness. Transfer responsibilities to Day-2 operations team. Obtain customer handover sign-off. | PM | Phase 4 | Not Started |

---

## Section 2: Risk Register

The NOVA Risk Register surfaces the key threats to schedule, quality, and customer confidence in the Bring-up & Validation phase. Each risk is tracked with an ID, likelihood/impact rating, early warning indicators, and PM-actionable mitigations. Assumptions, Issues, and Dependencies are tracked separately in the Wrike workspace as they emerge.

**Mandatory review cadence:** Weekly during Bring-up & Validation. Any High likelihood + High impact risk must be escalated immediately.

### 2.1 Risk Rating Key

| Rating | Likelihood | Impact | PM Action |
|---|---|---|---|
| High | Likely to occur | Program-level consequence | Immediate escalation; mitigation plan active |
| Medium / Medium-High | Possible | Significant delay or rework | Active monitoring: owner assigned; checkpoint review |
| Low | Unlikely | Minor or recoverable | Log and monitor; revisit at phase gate |

### 2.2 Risk Register

| Risk ID | Risk Description | Root Cause | Impact | Likelihood | Early Indicators | Mitigation / PM Actions | Owner |
|---|---|---|---|---|---|---|---|
| BUV-01 | Firmware versions not aligned across the cluster; OEM qualification delays block validation start. | OEM qualification delays; unclear upgrade ownership (OEM vs customer vs NVIS). | High | High | Mixed FW versions detected; Waiting on OEM approval; Blocked upgrades | Confirm target FW baseline pre-bring-up (T-02); Assign upgrade ownership explicitly; Secure maintenance windows early | PM / OEM Lead |
| BUV-02 | NVLink / InfiniBand fabric instability under full-scale load: slow racks, NVSwitch restarts, IB link flaps, BER events. | Scale-dependent HW/FW behavior not reproducible in small-scale labs. | High | High | Slow racks in burn-in; NCCL/HPL failures at load; BER / link flap events | Plan long-run validation early (T-16); Reserve exclusive access windows for stress testing (T-04); Escalate to fabric SMEs after 2 failed cycles | Validation Lead |
| BUV-03 | Shared customer cluster access limits validation: partial production use, restricted reboots, shortened test windows. | Customer workloads active during bring-up; limited maintenance windows. | Medium | Medium | Limited reboot access; Shortened test runs; Customer usage during validation windows | Negotiate validation blackout windows pre-engagement (T-04); Document validation vs production boundaries (T-01); Escalate to Account & PMO if blocked >5 days | PM |
| BUV-04 | Early-lifecycle platform (GB200 / GB300) maturity gaps: OS images, NCCL/HPL packages, kernel/driver mismatches not GA-ready. | OS, driver, and toolchain not fully GA at time of deployment. | Medium-High | Medium | Missing packages on delivery; Kernel/driver mismatch on power-on; Tooling automation gaps | Assess platform maturity pre-engagement (T-08); Reset customer expectations to 'joint engineering' framing when applicable; Label phase accurately in SOW and status reports | PM / Tech Lead |
| BUV-05 | Limited validation SME capacity vs. concurrent customer site and lab demand; expert bandwidth constrained. | Small pool of fabric/firmware/diagnostics specialists shared across programs. | Medium | Medium | Validation queues forming; Overlapping site demands; SME unavailable >1 week | Pre-book SMEs during program intake (T-05); Escalate resource conflicts to PMO immediately; Triage program priority with PMO Forum if contention persists | PM / PMO |
| BUV-06 | Manual validation steps introduce human error, inconsistent data capture, and longer root-cause cycles. | Tooling and automation gaps; reliance on ad-hoc scripts. | Medium | Medium | Repeated manual checks; Inconsistent data capture across sites; Re-runs caused by data gaps | Require use of approved NVIS tools/scripts exclusively (T-06); Mandate evidence artifacts for all validation steps (T-22); Log tooling gaps as improvement items in SNOW KB | Validation Lead |
| BUV-07 | Incomplete knowledge capture from bring-up; same issues recur across programs due to missing SNOW/NVBug entries. | Rapid execution pace; firefighting mode; missing KB entries at program close. | Medium | Low | Same bugs recurring across projects; Missing SNOW entries at close; No Tech Huddle readout completed | Require NVBug + SNOW KB entry as exit criterion (T-24); Mandate lessons-learned readout at Phase 4 close (T-25); PM to gate handover sign-off on KB completion | PM / Tech Lead |

---

## Section 3: Action Items

Action items are near-term, owner-assigned activities required to move the NOVA program from early planning into execution. All items should be tracked in Wrike (or equivalent) and reviewed at weekly PM syncs.

**Review cadence:** Weekly PM Sync. **Escalation:** Any item >1 week overdue must be escalated to Delivery Lead.

### 3.1 Immediate Actions (Week 1–2)

| AI ID | Action Item | Owner | Due Date | Linked Task / Risk | Status |
|---|---|---|---|---|---|
| AI-01 | Schedule NOVA program kickoff meeting with all stakeholders (PM, Tech Lead, Validation SMEs, PMO, customer counterpart). Set recurring cadence. | PM | Week 1 | T-01 | Not Started |
| AI-02 | Draft Scope Definition document: define Bring-up vs Validation vs Production boundaries. Circulate for customer sign-off. | PM | Week 1 | T-01 | Not Started |
| AI-03 | Identify and confirm Validation SME assignments. Flag any resource gaps or conflicts to PMO immediately. | PMO / PM | Week 1 | T-05 / BUV-05 | Not Started |
| AI-04 | Initiate firmware baseline inventory: collect current firmware versions across all cluster components. Identify mismatches. | SA | Week 1 | T-02 / BUV-01 | Not Started |
| AI-05 | Draft Escalation Path document: define owners, meeting touchpoints (Tech Huddle, PMO Forum, Customer Sync), and SLA thresholds. | PM | Week 1 | T-07 | Not Started |
| AI-06 | Open NOVA RAID log in Wrike (or equivalent). Pre-populate BUV-01 through BUV-07 as baseline risk entries. | PM | Week 1 | All Risks | Not Started |

### 3.2 Near-Term Actions (Week 2–4)

| AI ID | Action Item | Owner | Due Date | Linked Task / Risk | Status |
|---|---|---|---|---|---|
| AI-07 | Negotiate and lock customer validation blackout windows. Document agreed schedule in project plan and SOW addendum if needed. | PM | Week 2 | T-04 / BUV-03 | Not Started |
| AI-08 | Confirm OEM firmware qualification status. Escalate any pending qualifications to OEM Lead with target resolution date. | PM / OEM Lead | Week 2 | T-02 / BUV-01 | Not Started |
| AI-09 | Complete Bring-up Readiness RAG Assessment across all six dimensions (Firmware, Access, Platform Maturity, Resourcing, Tooling, Escalation). | PM | Week 2 | T-08 | Not Started |
| AI-10 | Confirm OS image and software stack readiness: validate NCCL, HPL, GPU FD, and ClusterKIT package availability and version alignment. | SA | Week 2 | T-03 / BUV-04 | Not Started |
| AI-11 | Validate remote access, UFM / BCManager deployment, and telemetry tooling (DCGM, ClusterMinder) are functional. | SA | Week 2 | T-06 | Not Started |
| AI-12 | Confirm platform maturity classification (GA vs early-lifecycle). If early-lifecycle, re-frame customer expectations to 'joint engineering' in all communications. | PM / Tech Lead | Week 3 | T-08 / BUV-04 | Not Started |
| AI-13 | Draft Validation Test Plan: define HPL/NCCL/ClusterKIT test scope, long-run burn-in duration, slow-rack criteria, and Go/No-Go thresholds. | PM / Validation SME | Week 3 | T-15 to T-20 | Not Started |
| AI-14 | Define evidence storage location and naming convention for all validation artifacts (Drive / SNOW / repo). Communicate to team. | PM | Week 3 | T-22 | Not Started |
| AI-15 | Schedule and communicate governance checkpoint calendar: Pre-Deployment Review, weekly Tech Huddles, PMO Forum, and Customer Syncs. | PM | Week 4 | All Sections | Not Started |
| AI-16 | Complete Program Plan baseline: confirm milestones, phase gates, and critical path in Wrike. Share with Delivery Lead for approval. | PM | Week 4 | All Tasks | Not Started |

---

## Section 4: Governance & Escalation Framework

NOVA program governance follows the standard NVIS PM framework: structured checkpoints, RAG-based phase gates, and a defined risk-to-escalation pathway that prevents surprise escalations.

### 4.1 RAG Readiness Scoring

RAG reflects readiness to **START or PROCEED**, not the amount of work completed. Review weekly during Bring-up & Validation.

| Dimension | Green ✅ | Amber ⚠️ | Red 🔴 |
|---|---|---|---|
| Firmware & Stack | Single approved baseline | Minor version skew | Mixed / unapproved versions |
| Cluster Access | Exclusive windows granted | Partial access | Shared / blocked access |
| Platform Maturity | GA and fully supported | Known gaps with workarounds | Pre-GA / unstable |
| Resourcing | SMEs confirmed and assigned | Partial coverage | No confirmed owners |
| Tooling & Evidence | Standard tools ready | Manual workarounds needed | Tooling missing |
| Escalation Readiness | Clear path and SLA defined | Path exists but informal | Undefined / no owner |

**Overall RAG rules:**
- **Green** = all dimensions Green or max 1 Amber
- **Amber** = 2+ Amber, no Red
- **Red** = any Red — may NOT proceed without PMO / Delivery Lead approval

### 4.2 Risk → Escalation Matrix

| Risk | Checkpoint Meeting | Trigger | Escalation Threshold |
|---|---|---|---|
| BUV-01 Firmware misalignment | Pre-Deployment Review | Baseline not locked | Escalate to PMO if not resolved by T-10 before bring-up |
| BUV-02 Fabric instability | NVIS Tech Huddle | Repeated slow rack / NCCL failures | Escalate to Engineering after 2 failed validation cycles |
| BUV-03 Shared cluster access | Customer Sync | Validation blocked >5 days | Escalate to Account Manager and PMO |
| BUV-04 Platform immaturity | Internal Kickoff | Missing OS image or tools at kickoff | Reclassify engagement as Joint Engineering; update SOW |
| BUV-05 Resource contention | PMO Forum | SME unavailable >1 week | PMO capacity escalation; triage program priority |
| BUV-06 Tooling gaps | Validation Review | Manual work causes re-runs or data loss | Log improvement in SNOW KB; approve risk to proceed or pause |
| BUV-07 Knowledge capture gaps | Phase 4 Gate Review | NVBug/SNOW entries missing at handover | Gate Phase 4 sign-off on KB completion; escalate to Tech Lead if entries outstanding at handover |

### 4.3 Standard Governance Flow

> **Risk Identified → RAID Log Updated → RAG Adjusted → Checkpoint Meeting → Escalation if Threshold Met**

### 4.4 Meeting Cadence

| Meeting | Frequency | Owner | Purpose |
|---|---|---|---|
| NOVA PM Weekly Sync | Weekly | PM | Task status, RAID review, RAG update, action item review |
| NVIS Tech Huddle | Weekly | Tech Lead | Technical escalations, fabric/firmware issues, lessons learned sharing |
| Customer Sync | Weekly during B&V | PM | Access windows, status update, expectation management |
| Pre-Deployment Review | Per program | PM / PMO | Phase 1 gate: confirm RAG Green/Amber before power-on |
| PMO Forum | Bi-weekly / on demand | PMO | Resource conflicts, program priority, capacity escalation |
| Phase Gate Reviews | End of each phase | PM / Delivery Lead | Entry/exit criteria sign-off; formal phase transition approval |

---

## Appendix: Quick Reference

### A. Owner Role Glossary

| Role | Responsibility |
|---|---|
| PM | Program Manager — owns schedule, RAID, customer communication, phase gates. |
| PMO | Program Management Office — resource allocation, portfolio-level escalation, governance. |
| SA | Solutions Architect — owns technical readiness, firmware/OS validation, tooling confirmation. |
| Tech Lead | Technical Lead — owns engineering decisions, escalation to NVIDIA Engineering, lessons learned. |
| Validation SME | Bring-up & Validation Specialist — owns test execution (HPL, NCCL, NV Qual, fabric diagnostics). |
| Fabric SME | Fabric Subject Matter Expert — owns NVLink, InfiniBand, and NVSwitch bring-up and diagnostics. |
| HW Team | Hardware Team — owns physical power-on, rack health, and hardware-layer issue resolution. |
| OEM Lead | OEM Partner Lead — owns OEM firmware qualification and partner-side upgrade coordination. |

### B. Status Definitions

| Status | Meaning |
|---|---|
| Not Started | Task / action item has not been initiated. |
| In Progress | Work has begun; expected to complete by due date. |
| Blocked | Task cannot proceed; dependency or risk is preventing progress. Escalate immediately. |
| Complete | Task fully done; exit criteria met and evidence filed. |
| Deferred | Intentionally postponed with PMO approval and revised due date. |

### C. Key NVIS Tools Reference

| Tool | Purpose |
|---|---|
| BCManager | Cluster management and bring-up automation scripts. |
| UFM / IBDiagnet | InfiniBand fabric management, health diagnostics, topology validation. |
| DCGM | GPU telemetry and monitoring during validation and operations. |
| ClusterKIT | NVIDIA-standard cluster validation and benchmarking suite. |
| NV Qual / GPU FD | NVIDIA field diagnostics and qualification testing tools. |
| HPL / NCCL | High-Performance LINPACK and NCCL benchmark suites for performance and fabric stress. |
| ClusterMinder | NVIS monitoring and telemetry tooling used during bring-up and validation. |
| ServiceNow (SNOW) | NVIS Knowledge Base for lessons learned and KB article management. |
| NVBug | NVIDIA internal bug tracking: mandatory for all bring-up and validation defects. |
| Wrike | Program task tracking; recommended for NOVA task and RAID log management. |

