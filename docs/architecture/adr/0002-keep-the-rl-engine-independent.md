# ADR 0002 — Keep the RL engine independent

Status: proposed  
Date: 2026-08-24

## Context

The existing `krybor_rl` Python package implements and tests the mathematical
behavior of bandits, finite MDPs, GridWorld, dynamic programming, and rollouts.
The planned web product needs interactive results but must not create a second,
quietly divergent implementation of those algorithms in TypeScript.

The engine must also remain useful for CLI experiments, future research work, and
tests without requiring a browser, HTTP server, database, or deployment platform.

## Decision

Keep `src/krybor_rl` framework-independent and make it the authoritative source for
RL computation.

- a stateless Python API imports the package and exposes bounded product use cases;
- the TypeScript web application consumes the API contract;
- TypeScript may calculate presentation-only state such as layout, animation, and
  input formatting;
- deterministic fixtures may support UI tests but integration tests verify the
  real engine;
- the RL engine never imports from `apps/` or `infra/`;
- application domains consume the engine rather than reshaping its core contracts.

## Consequences

Benefits:

- equations, experiments, CLI output, API results, and tests share one engine;
- the RL package remains inspectable and reusable;
- web-framework or infrastructure changes cannot force RL architecture changes;
- correctness work stays concentrated in one place.

Costs:

- interactive computation needs an API process or precomputed engine output;
- API contracts require serialization and versioning;
- offline-only browser behavior is limited unless a later ADR approves a safe
  compiled or duplicated subset with equivalence tests.

## Revisit when

Measured latency, offline requirements, or high-frequency interaction cannot be
served acceptably through the API and a concrete alternative preserves a single
testable source of mathematical truth.

