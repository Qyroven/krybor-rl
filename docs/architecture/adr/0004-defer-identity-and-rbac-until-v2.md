# ADR 0004 — Defer identity and RBAC until V2

Status: proposed  
Date: 2026-08-24

## Context

The long-term platform may support learners, instructors, content authors,
administrators, cohorts, assignments, and submissions. Those features require
authentication, authorization, persistent personal data, security operations,
privacy decisions, and backup and deletion policies.

The first product risk is not whether Krybor RL can store an account. It is whether
the structured, visual, executable learning experience can teach one coherent RL
module to someone other than its author.

## Decision

V1 is public and account-free.

- concept pages, the knowledge graph, learning paths, and labs require no login;
- completion state is stored locally in the browser and can be reset;
- there is no user database, remote submission, cohort, grading, or RBAC system;
- content authors use the Git and PR workflow;
- operational access is controlled by infrastructure identity and private
  networking, not application roles;
- identity and RBAC design begins only after V1 user testing establishes a need
  for cross-device progress, assignments, cohorts, or submissions.

## Consequences

Benefits:

- V1 concentrates on learning quality and mathematical interaction;
- the public content has no account barrier;
- the initial threat and privacy surface is smaller;
- backend and operations work are not dominated by generic account CRUD.

Costs:

- progress does not synchronize across browsers or devices;
- instructors cannot assign work to named learners;
- local completion is easy to alter and is not assessment evidence;
- later identity work will require deliberate data migration and privacy design.

## Entry conditions for V2 identity

Before implementation, a new ADR must define:

- concrete validated user workflows;
- identity provider and account-recovery responsibilities;
- role and permission matrix;
- data classification, retention, export, and deletion;
- audit, abuse, rate-limit, backup, and incident requirements;
- migration from local progress;
- operational ownership and cost.

