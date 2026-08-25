# Version 1 scope

Status: proposed and binding after acceptance  
Date: 2026-08-24

## Release objective

V1 proves that Krybor RL can teach one coherent unit as a public, visual,
interactive, and executable product. The vertical slice is Chapter 1 — Foundations.

V1 is not considered complete because a landing page exists. It is complete when
an independent learner can travel from the knowledge map through a guided path,
interact with the GridWorld, complete an assignment, and retain local progress.

## Included

### Product experience

- a concise public landing page;
- a Chapter 1 visual knowledge graph;
- concept pages generated from structured content;
- a Foundations learning path;
- navigation among prerequisites, related concepts, algorithms, and applications;
- browser-local progress with no account requirement;
- clear links from explanations to Python source and tests.

### Chapter 1 content

The initial graph contains at least:

- agent;
- environment;
- state;
- action;
- reward;
- return;
- objective;
- policy;
- value function;
- Markov property.

Every concept must satisfy the V1 subset of the content model: summary, intuition,
definition, relationships, one worked example or counterexample, code connection,
common mistake, and mastery check.

### Interactive experiences

#### Agent-environment loop

The learner can step through a GridWorld transition and inspect state, action,
actual movement after stochastic slip, reward, next state, and termination.

#### Reward-design laboratory

The learner can change one reward or uncertainty parameter, state a prediction,
solve the MDP through the Python engine, compare the policy and values, and explain
whether the objective, dynamics, or both changed.

### Technical system

- a TypeScript web application;
- a stateless Python API that imports `krybor_rl` rather than reimplementing it;
- the existing Python RL engine and CLI;
- structured content stored in the repository;
- Docker images for the web and API services;
- Docker Compose for the complete local runtime;
- CI for Python, content validation, web checks, container builds, and an
  integration smoke test;
- health endpoints and structured service logs.

### Documentation

- product and architecture specs;
- content authoring instructions;
- one-command local setup;
- an architecture diagram;
- a runbook for starting, stopping, checking, and troubleshooting V1 locally.

## Explicitly excluded

V1 does not include:

- registration, login, OAuth, or password management;
- cloud-synchronized user progress;
- a user database;
- learner, instructor, author, or administrator RBAC;
- cohorts, classrooms, submissions, grading, certificates, or payments;
- a content management system;
- AI tutoring or other LLM calls;
- Langfuse;
- Kubernetes;
- a multi-cloud deployment;
- distributed RL training;
- GPU orchestration;
- a comprehensive applications catalog;
- complete Chapters 2–4 migration into the web product.

These exclusions are not statements that the features have no value. They protect
the first proof of the learning experience.

## Delivery milestones

### Milestone 1 — Content foundation

- validate the concept metadata schema;
- author the ten Chapter 1 concepts;
- author one Foundations learning path and one assignment;
- resolve all prerequisite and relationship links.

### Milestone 2 — Readable product

- establish the web shell;
- render concept pages from content;
- render the knowledge graph and learning path;
- make navigation usable on desktop and mobile.

### Milestone 3 — Executable learning

- establish the stateless Python API boundary;
- implement the agent-environment stepper;
- implement the reward-design laboratory;
- connect outputs to the existing tested GridWorld and DP engine.

### Milestone 4 — Operable V1

- containerize web and API;
- start the stack with Docker Compose;
- expand CI across all V1 components;
- add health checks, structured logs, and a local operations runbook;
- conduct an external learner walkthrough and record findings.

## Acceptance criteria

V1 is releasable only when:

- all ten concepts pass schema and relationship validation;
- a new learner can finish the Foundations path without repository knowledge;
- the two interactive experiences work without handwritten result fixtures;
- central RL calculations come from the Python engine;
- progress survives a browser reload and can be reset explicitly;
- no account or remote personal data is required;
- Python, web, content, and integration checks pass in CI;
- `docker compose up` starts the documented local product;
- the repository contains no committed secrets;
- accessibility and responsive behavior receive an explicit review;
- the scope exclusions remain absent unless this document is amended.

## Change control

Any proposal that adds identity, a database, Kubernetes, an AI service, or another
large platform dependency before V1 completion must update this document and add
an architecture decision record explaining the blocking product need.

