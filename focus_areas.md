# Areas

> We validate GPU clusters, identify issues, and hand off findings — then move on. Our job is to determine whether a cluster is healthy before it goes to work.

## Observability

### Visualization (Grafana)

You are the person who turns raw numbers into something reviewable. The outcome is a set of time-series panels that make GPU health, job metrics, and bandwidth data legible at a glance. You will need to learn how Grafana works — building dashboards, writing PromQL queries, and organizing panels so the right information is visible without digging.

### Dashboarding (NVIS Rack Status)

You surface what is happening across the cluster in one place. The outcome is a live view of Slurm and Run:ai status that anyone on the team can read and act on, including the ability to launch validation workflows directly. You will need to learn how our tooling pulls data from those systems and how the dashboard is structured and extended.

### Metrics Collection & Telemetry Pipeline (DCGM / Prometheus)

You are responsible for getting GPU telemetry off the hardware and into a queryable form. The outcome is a reliable pipeline that collects per-GPU counters — utilization, temperature, power, Xid events, ECC and row-remap counts, NVLink CRC/replay errors, and thermal/clock-throttle reasons — and makes them available for comparison against thresholds. You will need to learn how DCGM exporters work, how Prometheus scrapes and stores metrics, and how to verify the pipeline is capturing what it should.

### Distributed Tracing & Profiling (Nsight Systems)

You capture what is actually happening inside a running multi-GPU job. The outcome is timeline traces that expose kernel stalls, communication bottlenecks, and synchronization overhead that aggregate metrics would miss. You will need to learn how to configure and run Nsight Systems, interpret the trace output, and identify the signatures of common GPU and interconnect problems.

## Validation

### NCCL

You understand the benchmarks that tell us whether the NVLink fabric is working correctly. The outcome is a measured pass or fail on collective communication health — all-reduce and all-to-all bandwidth across the NVL72 interconnect. You will need to learn how NCCL tests work, what bus bandwidth numbers to expect on this hardware, and how to distinguish a real fabric issue from a configuration or environment problem — including using RDMA point-to-point measurement (`perftest`) to localize whether a bad collective is the scale-up NVLink fabric or the scale-out network.

### LLMs and Models

You exercise the hardware the way real workloads will. The outcome is a confirmed result on whether the cluster can run a model training or inference job correctly — hitting expected throughput, producing numerically stable output. You will need to learn how to set up and run representative model workloads, what correct behavior looks like, and how to read the results as a signal of hardware health rather than model quality. You will need to understand TP, PP, DP, CP, and other tuning parameters for the models.

### System Architecture

You understand and validate how the hardware is put together. The outcome is documentation and verification of the topology — NVLink domains, NVSwitch connectivity, C2C paths, memory hierarchy, and the scale-out fabric topology and link state — so misconfigurations are caught before any job runs. You will need to learn how GB200/GB300 NVL72 systems are structured, how to query and interpret topology information (including read-only fabric queries such as `ibnetdiscover` and `ibdiagnet` to confirm the wiring matches intent and no links are down or degraded), and what a correctly configured system looks like versus one with a problem.

## Automation

### Health Checks

You build the gate that every node must pass before it gets used. The outcome is a lightweight pre-flight suite — GPU enumeration, NVLink link state, ECC, PCIe width, an Xid and error-counter scan, and a read-only check that driver, CUDA, and Fabric Manager state and versions are consistent across nodes — that can run quickly and block a bad node before a long job wastes time on it. You will need to learn what checks matter, how to implement them reliably across nodes, and how to surface failures in a way the rest of the pipeline can act on.

### Result Parsing

You bridge raw test output and structured data. The outcome is a reliable extractor that takes NCCL logs, nvbandwidth results, and Nsight reports and produces metrics that can be stored and compared. You will need to learn the output formats of the tools we use, how to handle variation and failure modes in that output, and how to write parsers that are robust enough to run unattended.

### Data Post-Processing (Data Lake)

You make results queryable over time and across deployments for us to gain a deeper understanding. The outcome is an aggregated store where parsed metrics from every run can be trended, compared across runs, and checked for regressions. You will need to learn how the data lake is structured, how results flow into it, and how to write queries that surface meaningful comparisons.

### Alerting & Threshold Management

You define what counts as a problem. The outcome is a set of pass/fail thresholds that cause dashboards to visually flag anomalies — including error-rate trending such as row-remap growth and NVLink replay-count climb, and thermal/clock-throttle thresholds — so whoever reviews the results can see at a glance what needs attention without interpreting raw numbers. You will need to learn what the expected ranges are for each metric on this hardware, how to configure thresholds in our tooling, and how to keep them calibrated as the cluster and workloads evolve.

### Test Launch

You own getting validation jobs onto the cluster and tracking them to completion. The outcome is a submission layer that handles Slurm job scheduling, dependency ordering, retries on transient failures, and status reporting back to the dashboards. You will need to learn how Slurm works, how our job definitions are structured, and how to make the launcher robust enough to run without constant supervision.
