# Target system architecture

Status: proposed  
Date: 2026-08-24

## Context

Krybor RL evolves from a Python learning repository into a public interactive
learning product without discarding the tested RL engine. The target system has
four primary assets:

- structured RL knowledge and learning compositions;
- a browser experience for reading, navigating, visualizing, and practicing;
- a Python computation service backed by the reusable `krybor_rl` package;
- versioned infrastructure used to test, deploy, secure, and observe the product.

## System context

```text
                        content author
                              |
                              v
                    Git repository and CI
                              |
                              v
learner --------------> Krybor RL web product
                              |
                              v
                     stateless Python API
                              |
                              v
                       krybor_rl engine
```

V1 stores learner completion state in the browser. There is no identity provider,
user database, instructor system, or remote personal progress store.

## Planned repository boundaries

```text
.
├── apps/
│   ├── web/                 # TypeScript browser product
│   └── api/                 # Python delivery service
├── content/                 # MDX plus validated metadata
├── learning/                # Paths, exercises, assignments, rubrics
├── src/krybor_rl/           # Reusable Python RL engine
├── labs/                    # Chapter-oriented reconstruction work
├── experiments/             # Reproducible experiment definitions
├── tests/                   # Python and cross-system correctness
├── infra/                   # Operable infrastructure definitions
└── docs/                    # Product, architecture, learning, runbooks
```

This is a target layout. Directories are created only when their first owned
artifact is implemented.

## Component responsibilities

### Structured content

Owns definitions, explanations, equations, typed relationships, references,
mastery outcomes, and connections to source code. It does not contain UI layout or
algorithm implementations.

### Web application

Owns routing, rendering, knowledge-graph interaction, visual explanations,
learning-path presentation, accessibility, and browser-local progress. It may
perform presentation-only calculations, but it must not become an independent
source of RL algorithm truth.

### Python API

Owns validation and translation between HTTP requests and application use cases.
It is stateless in V1 and imports the installed `krybor_rl` package. It does not
own formulas, environment mechanics, persistence, or frontend presentation.

### RL engine

Owns environments, agents, algorithms, trajectories, evaluation, experiment
semantics, and mathematical validation. It remains usable through Python and the
CLI without the web product.

### Infrastructure

Owns build, runtime, deployment, networking, configuration, observability,
security, backup, and operational automation. The RL engine never imports from
this layer.

## Dependency rules

```text
web -----------> content
 |                  |
 | HTTP             | validated references
 v                  v
API ------------> krybor_rl

infrastructure packages and operates web/API; it is not an application dependency
```

- `apps/api` may import `krybor_rl`; `krybor_rl` must not import `apps/api`.
- the web application calls a documented API contract for authoritative RL
  computation;
- generated fixtures may support deterministic UI tests but cannot replace
  integration checks against the engine;
- content references implementation symbols but does not execute source files;
- infrastructure treats applications as deployable artifacts and does not contain
  business or learning logic;
- applications and specializations consume the RL core through stable interfaces.

## Language ownership

| Technology | Ownership |
| --- | --- |
| Python | RL engine, experiments, API, mathematical tests |
| TypeScript | Web application and interactive presentation |
| MDX/Markdown | Narrative learning content and documentation |
| YAML | Content metadata, learning compositions, CI, Compose, Ansible, Kubernetes |
| HCL | OpenTofu infrastructure definitions |
| SQL | Persistent product data after V1 only |
| Shell | Small bootstrap and operational glue only |

New languages require an architecture decision record. Polyglot boundaries are a
consequence of responsibility, not a goal.

## V1 runtime

```text
browser
  |
  | HTTP
  v
web container
  |
  | HTTP/JSON
  v
API container
  |
  | in-process Python import
  v
krybor_rl package
```

Docker Compose provides the complete local runtime. The initial API has no
database connection and no remote user state.

## API design constraints

- endpoints express learning or experiment use cases rather than exposing Python
  objects directly;
- request parameters are bounded and validated;
- random behavior requires an explicit seed where reproducibility matters;
- responses identify algorithm/environment settings used to produce results;
- expensive operations receive resource limits before public exposure;
- the API contract is testable independently of the web application;
- health and readiness endpoints do not execute expensive RL workloads.

Likely V1 use cases include sampling one GridWorld transition, solving the rescue
GridWorld under specified parameters, and comparing values or policies across one
controlled parameter change. Concrete endpoint names belong to an API design ADR.

## Progress and data

V1 progress is intentionally local and non-sensitive:

```text
content revision + completed entity IDs + explicit reset control
```

The browser must tolerate removed or renamed draft content. No claim is made that
local completion proves mastery. Predictions and reflections remain learner-owned
unless a later product phase introduces explicit submissions.

## Security boundaries

- V1 accepts no user account credentials;
- secrets enter services through runtime configuration and never through Git;
- public API inputs are untrusted and validated;
- administrative endpoints are absent from V1;
- future operational dashboards and SSH access belong on a private network;
- containers run with the least privilege practical for their workload;
- dependencies, images, and infrastructure changes are reviewed in CI;
- deployment and rollback procedures are documented before public release.

## Observability boundaries

Three forms of evidence remain distinct:

| Evidence | Question answered |
| --- | --- |
| RL experiment results | Does the algorithm behave as claimed? |
| Service logs, metrics, traces | Is the platform operating reliably? |
| Future LLM traces/evaluations | Is an AI learning feature behaving acceptably? |

Langfuse is relevant only to the third category. It is not a replacement for
platform observability or RL experiment tracking.

## Evolution after V1

The system may later add identity, a database, cloud progress, instructor
workflows, asynchronous jobs, AI assistance, and Kubernetes. Each addition needs a
demonstrated product or operational requirement, a threat/data review, and an
accepted architecture decision record.

## Decisions intentionally left open

This specification fixes responsibilities before tools. Short implementation
spikes and separate ADRs should decide:

- the TypeScript web framework;
- the Python API framework;
- the concrete MDX/YAML schema and validation tool;
- the graph layout and visualization libraries;
- the first public hosting and cloud provider;
- the API versioning and generated-client approach.

Selection criteria must include clarity for learners, integration with the Python
engine, accessibility, testability, operational burden, security, cost, and exit
cost. Framework popularity alone is not sufficient.
