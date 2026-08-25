# Infrastructure learning and delivery roadmap

Status: proposed  
Date: 2026-08-24

## Mission

Operating Krybor RL is a supporting learning track for Linux, networking, cloud,
automation, security, reliability, and ML infrastructure. Every infrastructure
milestone must both improve the real platform and preserve evidence of what was
learned.

Infrastructure does not expand the educational subject of V1 beyond RL. It is the
professional engineering system beneath the RL product and may later become a
public “how Krybor RL is built” track.

## Principles

- start with the smallest topology that serves the current product;
- automate a manual process only after understanding it;
- keep local development possible without cloud access;
- separate public traffic from private operational access;
- provision repeatable resources as code;
- store no plaintext secret in Git, images, logs, or experiment results;
- test backup restoration, not only backup creation;
- attach cost, security, observability, rollback, and runbook concerns to changes;
- do not make Kubernetes a prerequisite for learning RL;
- introduce LLM observability only with an actual LLM feature.

## Evidence required per milestone

An infrastructure topic is complete only when it includes:

- the problem and assumptions;
- an architecture or network diagram;
- versioned configuration;
- an automated validation or smoke test;
- a deployment and rollback procedure;
- a troubleshooting runbook;
- security and secret-handling notes;
- cost and cleanup notes for external resources;
- a short reflection explaining a failure or corrected mental model.

## Stage 0 — Repository baseline

Current evidence:

- Python packaging;
- unit and CLI smoke tests;
- GitHub Actions CI on supported Python versions;
- reproducible experiment configuration;
- no runtime dependency and no deployment target.

Exit condition: platform V1 scope and system boundaries are accepted.

## Stage 1 — Local application runtime

Product need: run the web product and Python API consistently on contributor
machines and in integration tests.

Learn:

- image layers and multi-stage builds;
- container users and file permissions;
- networks, ports, volumes, and environment configuration;
- health checks and process lifecycle;
- development versus production image concerns;
- image tagging and registry basics.

Deliver:

- separate web and API Dockerfiles;
- `compose.yaml` for the complete local product;
- health checks and dependency-aware startup;
- a containerized integration smoke test;
- documented native and container workflows.

Exit condition: a clean machine with Docker can start and verify V1 through one
documented command.

## Stage 2 — One Linux server

Product need: host a public preview without the complexity of orchestration.

Learn:

- Linux users, groups, permissions, processes, signals, and services;
- SSH keys and access hardening;
- package updates, firewall, disk, memory, CPU, and logs;
- IPv4/IPv6, ports, DNS records, HTTP, TLS, and reverse proxies;
- service restart, log rotation, backup, and restore.

Deliver:

- one staging VPS;
- DNS and HTTPS;
- a reverse proxy in front of Compose services;
- public web/API endpoints and no public operational dashboards;
- server bootstrap and incident runbooks;
- automated backup plus a successful restore drill.

Exit condition: the preview survives reboot, exposes only intended ports, renews
TLS automatically, and can be restored from documented artifacts.

## Stage 3 — Private network and configuration automation

Product need: operate the server and future monitoring services without exposing
administrative interfaces publicly.

Learn:

- routing, subnets, NAT, firewall policy, and private addressing;
- VPN concepts and WireGuard fundamentals;
- identity-aware mesh networking and access policy;
- configuration management, inventory, idempotence, and drift.

Deliver:

- private access for SSH and operational services through Tailscale;
- one manual WireGuard lab to understand the underlying network model;
- Ansible inventory, roles, and playbooks for server configuration;
- repeatable user, firewall, Docker, reverse-proxy, VPN, backup, and update setup;
- a test proving a second configuration run is idempotent.

Exit condition: a replacement server can be configured from a documented base OS
using versioned automation and without public admin ports.

## Stage 4 — Infrastructure as Code and continuous delivery

Product need: reproduce external resources and deliver reviewed revisions without
console-only state.

Learn:

- declarative infrastructure and dependency graphs;
- provider versions, state, drift, plan, apply, import, and destroy;
- remote state and secret boundaries;
- environments, release promotion, rollback, and deployment identity;
- artifact immutability and software supply-chain basics.

Deliver:

- OpenTofu definitions for compute, network, firewall, DNS, and backup storage;
- separated staging and production configuration;
- CI format, validate, and speculative plan checks;
- versioned application images in a registry;
- deployment automation following the repository branching strategy;
- a rollback to a previously known-good image.

Exit condition: infrastructure and application changes are reviewable before
mutation, and production can be recreated without undocumented console steps.

## Stage 5 — Platform observability and reliability

Product need: answer whether users can access and use the learning experience and
diagnose failures without adding emergency instrumentation.

Learn:

- structured logs, metrics, traces, and correlation;
- request rate, errors, duration, saturation, and resource metrics;
- OpenTelemetry instrumentation and collection;
- Prometheus-style metrics, dashboards, alerting, SLI, SLO, and error budgets;
- load testing, incident response, postmortems, and capacity planning.

Deliver:

- correlation IDs and structured logs;
- service and infrastructure metrics;
- end-to-end traces for representative web-to-API requests;
- private dashboards and actionable alerts;
- one availability SLI/SLO and one latency SLI/SLO;
- a load test, failure exercise, incident runbook, and postmortem.

Exit condition: a deliberately introduced failure is detected, diagnosed, and
recovered through documented signals and procedures.

## Stage 6 — Cloud foundation

Product need: learn and operate managed infrastructure when the single-server
topology becomes a constraint or when a cloud learning objective is selected.

Choose one primary cloud before adding a second. The initial learning surface
should cover:

- IAM and least privilege;
- virtual networks, public/private subnets, routes, gateways, and security groups;
- compute and autoscaling concepts;
- object storage and lifecycle policy;
- container registry;
- load balancing and managed DNS;
- managed database only after persistent product data exists;
- secrets, audit logs, budgets, quotas, and cost alerts;
- regional failure, backup, and recovery trade-offs.

Deliver:

- OpenTofu modules with constrained provider versions;
- a staging environment created and destroyed from code;
- architecture, threat, cost, and recovery documents;
- automated budget alerts and cleanup instructions;
- a comparison explaining which managed services replace self-operated components.

Exit condition: the chosen cloud deployment has an explicit advantage over the
single server and no forgotten unbounded resource.

## Stage 7 — Kubernetes

Product need: learn orchestration or solve a demonstrated multi-service scaling,
availability, or workload-scheduling problem.

Progression:

```text
Docker Compose
→ local or single-node K3s
→ multi-node K3s
→ managed Kubernetes comparison
```

Learn:

- Pods, Deployments, Services, Ingress, and namespaces;
- ConfigMaps, Secrets, probes, requests, limits, and quotas;
- persistent volumes and state boundaries;
- cluster DNS, CNI, network policy, and service exposure;
- Jobs, CronJobs, rolling updates, autoscaling, and disruption;
- Kustomize or Helm packaging;
- GitOps and cluster upgrade/recovery responsibilities.

Deliver:

- local K3s deployment of the existing images;
- base manifests plus environment overlays;
- network policy and private operations access;
- GitOps only after manual deployment is understood;
- upgrade, rollback, node-failure, and cluster-recovery exercises;
- a written comparison with the simpler Compose topology.

Exit condition: Kubernetes demonstrably teaches or solves a problem worth its
operational cost and remains optional for ordinary learners.

## Stage 8 — Identity and data operations

Product need: V2 cloud progress, assignments, cohorts, or submissions.

Learn and deliver:

- authentication versus authorization;
- learner, instructor, author, and administrator permissions;
- relational data modeling and migrations;
- encryption, retention, deletion, audit, and privacy boundaries;
- database pooling, backup, restore, and schema rollback;
- threat modeling and abuse controls.

This stage cannot begin merely to make V1 look like a platform.

## Stage 9 — AI and RL workload infrastructure

Product need: a validated AI tutor or compute workload beyond synchronous tabular
experiments.

Potential learning areas:

- LLM prompt, trace, token, cost, feedback, and evaluation management with
  Langfuse or an equivalent system;
- RL experiment tracking, artifact storage, checkpointing, and model registry;
- queues, workers, scheduled and batch jobs;
- GPU hosts, device plugins, container runtimes, utilization, and cost controls;
- distributed training and fault-tolerant jobs only after single-node baselines;
- inference deployment only for a real model-serving use case.

Langfuse does not replace platform telemetry, and RL experiment tracking does not
replace either of them.

## Tool admission checklist

Before adding a tool, record:

1. the current problem and evidence that it exists;
2. the simplest alternative;
3. the owner and operational burden;
4. data, network, credential, and cost implications;
5. local and CI validation;
6. failure, rollback, backup, and removal procedures;
7. the learning outcome produced by adopting it.

If these answers are vague, the tool remains in the roadmap rather than the
runtime.

