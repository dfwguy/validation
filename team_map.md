# Overall Leads

- Travis Drake
- Harish Lakshminarasimhan
- Rafael Marcelino Koike

# Project Streams -- Teams and Descriptions

We are using Team Topologies to organize three teams around the streams below. Working on Projects is the fourth stream, shared by everyone. People can work on specific tools and move between streams as we learn what each project requires.

We will aim to have someone from each of the three streams on every customer project. Performance Engineering and Data Engineering are currently light on staffing, and a plan to address that is still to be determined. We will adjust responsibilities and boundaries as the work develops.

Team calls will be organized around these streams. The aim is to establish clear boundaries, collaborate where needed, and develop services that other streams can consume in the workflow.

People are listed under each stream’s “Who?” section. For projects shared across streams, each project entry describes that stream’s responsibility. Initial stream membership is inferred from the previous tool and SME rosters; people may work across streams. Entries labeled **Proposed** are starting points for review. All projects support the shared Working on Projects stream.

## Working on Projects -- Testing, Validation, and Benchmarking

### Description

This is our main job and we will all be doing doing it. As things evolve, we will be ensuring that tests are running and doing any initial triage on what can be fixed or done to make them go more smoothly. Sometimes, things will be fully automated, but when they aren't we need to work with each on the team assigned to the project to ensure that tests run smoothly and we are getting the results we expect. This will involve understanding the basics of Slurm, our tests, what system state should look like, and the tools we build.

### Who?

**Everyone**

### Tools

The whole stack

### Interactions with Other Streams

- Work with Installation and Data to get the cluster, access, and data ready for testing.
- Use the interfaces, scripts, and tests provided by User Interfaces, Triage, and Scripts to run tests and perform initial triage.
- Work with Performance Engineering and Data Engineering to investigate low performance, tune tests, and interpret results.

## Installation and Data

### Description

This is the group that will be focused on cluster bring-up as well as getting it so we have all of the data available for other teams. This will be a cross functional team that has to work with teams such as Ethernet, InfiniBand, and NVLink Switches in order to get OpenTelemetry and other data available for teams to consume. You will be the vanguard on making sure the cluster is ready for us to begin testing on and you will collaborate with the AIC team to ensure everyone else can login and we have enough resources (space on filesystem, CPUs, RAM, and network.)

#### Project Responsibility

- You will not own Grafana, but you will own Prometheus and Victoria Metrics.
- You will not own NVIS Rack Status but you will own the API that sits beneath it
  - Future item, NVIS Rack Status should split into at least two project, with the WebUI being separate from the API
  - Auto Trigger results will be on the filesystem but eventually should be consumed through the Rack Status API
- You will ensure Auto Trigger is running and its data is available
- You will own NVIS P2P and ensuring that the containers and any other files we need are distributed
- You will collaborate across NVIS, including functions such as CVT, to make the data needed for validation available.
- This stream ends in an API that provides consistent access to the data for other streams.

### Who?

- Harish Lakshminarasimhan
- Rafael Marcelino Koike
- Michael Echavarria
- New Hire
- Travis Drake
- Dejaun Gayle
- Tyler Race
- Alyssa Sawyer

### Tools

- Telemetry consumed for Observability
  - Data stores
    - Prometheus
    - Victoria Metrics
  - API for access consistency
- NVIS Rack Status - API and data sources
- Auto Action Trigger
- NVIS P2P

### Projects

- **NVIS Rack Status — API and data sources**.
- **Observability — telemetry, Prometheus, and Victoria Metrics**.
- **Auto Action Trigger — operation and data availability**.
- **NVIS P2P**.

### Interactions with Other Streams

- Collaborate with User Interfaces, Triage, and Scripts
- Provide the API and data service consumed by User Interfaces, Triage, and Scripts.
- Collaborate with AIC and across NVIS, including Ethernet, InfiniBand, NVLink Switches, and CVT, on cluster readiness and data availability.
- Support Working on Projects by ensuring the cluster and data are ready for testing.

## User Interfaces, Triage, and Scripts

### Description

This is the group that makes the data visible and builds the interfaces we use in our work. You will own scripts that automate triage, determine which tests we need to run, and ensure those tests are optimal. You will use the API and data service provided by Installation and Data to build a service that Performance Engineering and Data Engineering can consume.

#### Project Responsibility

- You will own Grafana dashboards and the visualization of telemetry provided by Installation and Data.
- You will own the NVIS Rack Status WebUI and consume the API provided by Installation and Data.
- You will build and maintain scripts that automate triage and help the team run the right tests.
- You will determine which tests we need to run and ensure they are optimal, incorporating findings from Performance Engineering and Data Engineering.
- This stream ends in user interfaces, including CLIs, WebUIs, and MCPs.

### Who?

- Rafael Marcelino Koike
- Harish Lakshminarasimhan
- Michael Echavarria
- Michelle Ramirez
- Travis Drake
- Yugandhar Khair
- Dejaun Gayle
- Tyler Race
- Alyssa Sawyer
- New Hire

### Tools

- Grafana
- NVIS Rack Status - WebUI
- Software Factory
- Documentation Tooling
- Auto Action Trigger - testing and conformance workflows
- CLIs, WebUIs, and MCPs for validation workflows
- Triage automation scripts and test workflows

### Projects

- **NVIS Rack Status — WebUI**.
- **Observability — Grafana and visualization**.
- **Software Factory (Proposed)** — automation of test workflows.
- **Documentation Tooling (Proposed)** — publishing and accessing team documentation.
- **Auto Action Trigger — Testing and Conformance:** test selection and triage automation.

### Interactions with Other Streams

- Consume the API and data service provided by Installation and Data.
- Provide interfaces, scripts, and tests as a service to Performance Engineering and Data Engineering.
- Support Working on Projects with interfaces for running tests, reviewing results, and performing initial triage.
- Collaborate with RoW to ensure we are aligned.

## Performance Engineering and Data Engineering

### Description

This is the group that learns within and across projects where we should focus fixes and how to dial in tests so they pass. You will be the primary source of help for understanding tests that run but produce low performance. You will turn results into evidence that supports decisions during customer engagements and builds our understanding across projects.

#### Project Responsibility

- You will investigate low performance and help the project team understand what the test results mean.
- You will identify where to focus fixes and how to tune tests to meet expected performance.
- You will learn across projects and make results available for analysis and comparison through the data lake.
- You will produce charts, Jupyter notebooks, decisions during engagements, and whitepapers that explain findings and guide future work.
- This stream ends in a data lake and the analysis and decisions built from it.

### Who?

Performance Engineering and Data Engineering are currently light on staffing; the staffing plan remains to be determined.

- Harish Lakshminarasimhan
- New Hire
- Rafael Marcelino Koike (NCCL SME)
- Alyssa Sawyer
- Bryan Reese (Temporary)

### Tools

- NVIS Data Lake
- Charts and Jupyter notebooks
- NCCL, LLM Debug, and Network Performance expertise within the stream
- Interfaces, scripts, and tests provided by User Interfaces, Triage, and Scripts

### Projects

- **NVIS Data Lake**.
- **NCCL (Proposed)** — performance expertise and collaboration with User Interfaces, Triage, and Scripts on test selection and tuning.
- **LLM Debug (Proposed)** — investigation of workload behavior and low performance during projects.
- **Network Performance (Proposed)** — performance investigations and collaboration with Installation and Data on network readiness or telemetry.

### Interactions with Other Streams

- Consume the service provided by User Interfaces, Triage, and Scripts.
- Feed findings back to User Interfaces, Triage, and Scripts to improve test selection, tuning, and triage automation.
- Support Working on Projects with performance investigations and decisions during engagements.
- Collaborate with DRE.
