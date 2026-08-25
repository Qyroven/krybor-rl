# ADR 0001 — Use a polyglot monorepo

Status: proposed  
Date: 2026-08-24

## Context

Krybor RL already contains a Python engine, experiments, tests, labs, and learning
artifacts. The target product adds a TypeScript web application, a Python API,
structured content, and infrastructure definitions. These components evolve
together and share contracts, releases, and educational examples.

Splitting them into repositories now would require cross-repository coordination
before team size, access boundaries, or independent release schedules justify it.
Using one language for every responsibility would either weaken the browser
experience or duplicate the Python RL engine.

## Decision

Use one polyglot monorepo with explicit ownership boundaries:

- Python for the RL engine, experiments, API, and mathematical tests;
- TypeScript for the web product and interactive presentation;
- MDX/Markdown and YAML for structured learning content;
- YAML and HCL for infrastructure and delivery;
- SQL only when persistent product data exists after V1;
- Shell only for small bootstrap or operational glue.

CI will run component-specific checks and integration checks based on the same
revision. A new general-purpose programming language requires another ADR.

## Consequences

Benefits:

- one revision connects content, implementation, visualization, tests, and infra;
- atomic changes can update contracts and consumers together;
- contributors have one place to inspect the whole learning system;
- local and CI integration testing is simpler.

Costs:

- tooling and dependency management span several ecosystems;
- CI must avoid rebuilding every component unnecessarily as the repository grows;
- ownership rules must prevent application and infrastructure concerns from
  leaking into the RL engine.

## Revisit when

A component needs independent access control, release cadence, compliance
boundary, ownership, or scale that creates more coordination inside the monorepo
than across repositories.

