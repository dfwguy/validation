# Overall Leads

## Description

Working across projects, the overall leads are expected to have an overall idea of how everything works together. They will be the best point of contact for questions on scheduling and resolving technical questions, either by knowing the answer or knowing where to go to get the answer.

Expect the overall leads to have the area they are the SME in.

## Who

- Travis Drake
- Harish Lakshminarasimhan
- Rafael Marcelino Koike

# Project Streams -- Teams and Descriptions

We are using [Team Topologies](https://itrevolution.com/wp-content/uploads/2022/06/TTOP_audio-excerpt_072419_r1.pdf) to organize three teams around the streams below. Working on Projects is the fourth stream, shared by everyone. People can work on specific tools and move between streams as we learn what each project requires.

We will aim to have someone from each of the three streams on every customer project. We will adjust responsibilities and boundaries as the work develops.

Team calls will be organized around these streams. The aim is to establish clear boundaries, collaborate where needed, and develop services that other streams can consume in the workflow.

People are listed under each stream’s “Who?” section. For projects shared across streams, each project entry describes that stream’s responsibility. All projects support the shared Working on Projects stream.

## Shared Repository and Review Ownership

We intend to bring NVIS Rack Status and Auto Action Trigger into one repository, with clear directories for the API and data access, user interfaces, shared validation tests and verdicts, and cluster-side execution. This is a target model; the existing repositories and integration remain in place until migration is planned and verified. A shared repository does not require a single service, release, or deployment: the API, user interfaces, and cluster-side execution can retain independent build and deployment paths.

Each area has a primary owning stream. GitLab directory ownership and merge request approval rules should require review from the responsible stream for changes in its area. Changes across areas need review from each affected stream. Installation and Data reviews changes to API contracts and source-data schemas; the consuming streams also review changes that affect their use. Ownership rules must cover contracts and schemas wherever they live, not just files in an API directory. Verify that GitLab approval settings enforce the intended reviews, including for changes spanning multiple areas. AI-assisted changes follow the same review process.

Installation and Data owns the versioned source-data API and its contract. User Interfaces, Triage, and Scripts and Performance Engineering and Data Engineering are consumers and help define their data and compatibility requirements. Maintain compatibility and migration guidance for API changes because components and consumers may be deployed on different schedules. Performance Engineering and Data Engineering continues to own data lake ingestion and analysis.

Shared validation checks, benchmark implementations, and their verdict rules should have one canonical source in the shared repository, used by Auto Action Trigger and surfaced by Rack Status. User Interfaces, Triage, and Scripts owns test content and workflows; Installation and Data owns cluster-side installation, operation, and execution infrastructure. Performance Engineering and Data Engineering reviews test thresholds and interpretation where relevant. Rack Status may retain operator workflows while using the shared tests and results through a supported interface.

Migrate tests incrementally: inventory and compare existing checks, preserve distinct platform and multi-node capabilities, and verify equivalent behavior and results on representative hardware before retiring duplicates. Preserve site-specific baselines and verdict semantics. Define a supported interface for requesting runs and obtaining status, verdicts, and evidence; existing filesystem and reporting-script integrations remain until a replacement is ready.

## Working on Projects -- Testing, Validation, and Benchmarking

### Description

This is our main job and we will all be doing doing it. As things evolve, we will be ensuring that tests are running and doing any initial triage on what can be fixed or done to make them go more smoothly. Sometimes, things will be fully automated, but when they aren't we need to work with each on the team assigned to the project to ensure that tests run smoothly and we are getting the results we expect. This will involve understanding the basics of Slurm, our tests, what system state should look like, and the tools we build.

### Who?

**Everyone**

### Tools

The whole stack

## Installation and Data

### Description

This is the group that will be focused on cluster bring-up as well as getting it so we have all of the data available for other teams. This will be a cross functional team that has to work with teams such as Ethernet, InfiniBand, and NVLink Switches in order to get OpenTelemetry and other data available for teams to consume. You will be the vanguard on making sure the cluster is ready for us to begin testing on and you will collaborate with the AIC team to ensure everyone else can login and we have enough resources (space on filesystem, CPUs, RAM, and network.)

#### Project Responsibility

- You will own telemetry collection, Prometheus, and Victoria Metrics, and provide data for Grafana dashboards owned by User Interfaces, Triage, and Scripts.
- You will own the NVIS Rack Status API and data sources. User Interfaces, Triage, and Scripts owns the WebUI. The API and WebUI can remain in the same repository with directory-level review ownership.
  - Auto Action Trigger results are available through existing filesystem and reporting-script integration; a supported interface for runs and results is a target for the shared repository.
- You will own getting Auto Action Trigger installed and running on the cluster and making its results available. User Interfaces, Triage, and Scripts owns the tests and conformance testing (formerly health checks) that it runs.
- You will own NVIS P2P and distribution of containers and other files needed for testing.
- You will collaborate across NVIS, including functions such as CVT, to make the data needed for validation available.
- You will provide source data and consistent API access for interfaces and analysis. Performance Engineering and Data Engineering owns ingestion into the data lake using Parquet files exported from the cluster, along with the data lake and analysis built from it.
- This stream provides consistent API access to cluster data and supports the source-data handoff for Parquet-based data lake ingestion.

### Who?

- Harish Lakshminarasimhan
- Michael Echavarria
- Michelle Ramirez

### Tools and Capabilities

- Telemetry consumed for Observability
  - Data stores
    - Prometheus
    - Victoria Metrics
  - API for access consistency
- NVIS Rack Status - API and data sources
- Auto Action Trigger
- NVIS P2P

### Projects

- **NVIS Rack Status** — own the API and data sources; the API and WebUI can share a repository with separate review owners.
- **Observability** — collect telemetry and operate Prometheus and Victoria Metrics for downstream visualization and analysis.
- **Auto Action Trigger** — own installation and operation on the cluster and make test results available; User Interfaces, Triage, and Scripts owns the tests and conformance testing it runs.
- **NVIS P2P** — distribute containers and other files needed for testing.

### Interactions with Other Streams

- Provide APIs and data consumed by User Interfaces, Triage, and Scripts; incorporate feedback on data access and completeness.
- Provide source data for Performance Engineering and Data Engineering, which owns data lake ingestion using Parquet files exported from the cluster; collaborate on network readiness, telemetry, and data needed for performance investigations and cross-project analysis.
- Collaborate with AIC and across NVIS, including Ethernet, InfiniBand, NVLink Switches, and CVT, on cluster readiness and data availability.
- Support Working on Projects by ensuring the cluster and data are ready for testing and resolving readiness, installation, and data availability issues identified during initial triage.

## User Interfaces, Triage, and Scripts

### Description

This is the group that makes the data visible and builds the interfaces we use in our work. You will own the tests, conformance testing (formerly health checks), and scripts that automate triage. You will select and maintain test workflows, incorporating performance findings from Performance Engineering and Data Engineering. You will use the APIs and data provided by Installation and Data to deliver interfaces, scripts, and tests for project teams and Performance Engineering and Data Engineering.

#### Project Responsibility

- You will own Grafana dashboards and the visualization of telemetry provided by Installation and Data.
- You will own the NVIS Rack Status WebUI and consume the API provided by Installation and Data.
- You will build and maintain scripts that automate triage and help the team run the right tests.
- You will own test implementation, selection, and configuration, including conformance testing. You will incorporate tuning recommendations and performance validation from Performance Engineering and Data Engineering.
- Shared tests and verdict rules have one canonical source in the shared repository and are used by Auto Action Trigger and Rack Status. This stream owns test content regardless of execution infrastructure.
- For the proposed Software Factory project, the intended scope is automation of test workflows.
- For the proposed Documentation Tooling project, the intended scope is publishing and accessing team documentation.
- This stream ends in user interfaces, including CLIs, WebUIs, and MCPs.

### Who?

- Travis Drake
- Yugandhar Khair
- Dejaun Gayle

### Tools and Capabilities

- Grafana
- NVIS Rack Status - WebUI
- Software Factory (Proposed)
- Documentation Tooling (Proposed)
- Tests and conformance workflows run by Auto Action Trigger
- CLIs, WebUIs, and MCPs for validation workflows
- Triage automation scripts and test workflows

### Projects

- **NVIS Rack Status** — own the WebUI and consume the API provided by Installation and Data; the API and WebUI can share a repository with separate review owners.
- **Observability** — own Grafana dashboards and visualization of telemetry provided by Installation and Data.
- **Software Factory (Proposed)** — automation of test workflows.
- **Documentation Tooling (Proposed)** — publishing and accessing team documentation.
- **Tests and Conformance** — own tests, conformance testing, test selection and configuration, and triage automation, including workflows run by Auto Action Trigger. Shared test implementations and verdict rules have one canonical source in the shared repository.

### Interactions with Other Streams

- Consume the API and data service provided by Installation and Data.
- Provide interfaces, scripts, and tests to Performance Engineering and Data Engineering; incorporate its findings into test selection, configuration, and triage automation.
- Support Working on Projects with interfaces for running tests, reviewing results, and performing initial triage. Project teams perform initial triage; this stream resolves issues in interfaces, tests, conformance workflows, and automation.
- Collaborate with Rest of World (RoW) to ensure alignment.

## Performance Engineering and Data Engineering

### Description

This is the group that learns within and across projects where we should focus fixes and how to tune systems and test configurations to meet expected performance. You will be the primary source of help for understanding tests that run but produce low performance. You will turn results into evidence that supports decisions during customer engagements and builds our understanding across projects.

#### Project Responsibility

- You will investigate low performance and help the project team understand what the test results mean during a customer engagement.
- You will identify where to focus fixes, recommend system and test configuration changes, and validate their performance impact. User Interfaces, Triage, and Scripts owns implementation of changes to shared tests and workflows.
- You will own the NVIS Data Lake, ingestion into it using Parquet files exported from the cluster, and cross-project analysis. Installation and Data provides the source data and consistent API access for cluster workflows.
- You will develop documented analysis methods and reusable sample functions for working with data on the cluster and in the data lake.
- You will produce charts, Jupyter notebooks, decisions during engagements, and whitepapers that explain findings and guide future work.
- This stream ends in a data lake and the analysis and decisions built from it.

### Who?

- Tyler Race
- Rafael Marcelino Koike
- Alyssa Sawyer
- Bryan Reese (Temporary)

### Tools and Capabilities

- NVIS Data Lake
- Parquet files exported from the cluster for data lake ingestion
- Charts and Jupyter notebooks
- NCCL, LLM Debug, and Network Performance expertise within the stream
- Interfaces, scripts, and tests provided by User Interfaces, Triage, and Scripts

### Projects

- **NVIS Data Lake** — own ingestion of Parquet files exported from the cluster and the data lake used for cross-project analysis and comparison.
- **Documented Analysis and Sample Functions** — produce repeatable analysis methods, example notebooks, and reusable functions for cluster and data lake analysis beyond Grafana dashboards.

#### Skill Areas We Need to Scale

- **NCCL** — performance expertise and collaboration with User Interfaces, Triage, and Scripts on test selection and tuning.
- **LLM Debug** — investigation of workload behavior and low performance during projects.
- **Network Performance** — performance investigations and collaboration with Installation and Data on network readiness or telemetry.

### Interactions with Other Streams

- Consume interfaces, scripts, and tests provided by User Interfaces, Triage, and Scripts; return findings and tuning recommendations to improve test selection, configuration, and triage automation.
- Ingest Parquet files exported from the cluster into the data lake, using source data provided by Installation and Data; collaborate on network readiness, telemetry, and data needed for performance investigations and cross-project analysis.
- Support Working on Projects with performance investigations and decisions during engagements. Project teams perform initial triage and bring tests that run but produce low performance to this stream for deeper investigation.
- Collaborate with Deployment Readiness Engineering (DRE).
