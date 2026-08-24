# ADR 0003 — Use main, develop, and short-lived branches

Status: proposed  
Date: 2026-08-24

## Context

The repository currently uses `main` as its default and only permanent branch.
The target product will eventually have a continuously deployable production
revision and a shared integration revision. Creating a second default-style branch
named `master` solely for specifications would make authority and deployment state
ambiguous.

Documentation changes can alter product scope, security assumptions, contracts,
and operations. They need the same review and history discipline as code.

## Decision

Use the following branch roles after this specification is accepted:

- `main` is the protected production and release branch;
- `develop` is the protected integration branch for the next release;
- `feature/*`, `fix/*`, `docs/*`, and `infra/*` are short-lived branches;
- ordinary branches start from `develop` and merge into `develop` through PRs;
- a release PR promotes `develop` to `main` after all release checks pass;
- `hotfix/*` starts from `main`, merges to `main`, and is then reconciled into
  `develop`;
- no permanent `master` or `dev` alias is created;
- direct pushes to `main` and `develop` are prohibited once branch protection is
  configured;
- specification and documentation changes follow the same PR flow as code.

Before `develop` exists, the initial platform specification branch may target
`main`. After that merge, create `develop` from the accepted `main` revision.

## Delivery behavior

Planned mapping:

```text
pull request to develop → full CI and optional preview
merge to develop        → integration build and staging deployment
release PR to main      → release checks
merge to main           → immutable production deployment
```

Production deployment must use the tested merge commit or an immutable artifact
built from it. Environment secrets remain outside Git.

## Consequences

Benefits:

- `main` has one unambiguous meaning: releasable production state;
- integration work can accumulate without pretending each merge is a release;
- specs, code, content, and infrastructure use one review model;
- release and hotfix history remain inspectable.

Costs:

- long-lived `develop` can drift from `main` or accumulate unstable work;
- release promotion adds ceremony for a personal project;
- branch protection and CI must be maintained.

Mitigations:

- keep changes and release intervals small;
- prefer feature flags or incomplete unpublished content over long-lived branches;
- remove `develop` in a future ADR if continuous deployment from `main` becomes
  simpler and equally safe.

## Rejected alternatives

### Put specifications on `master` and deploy from `main`

Rejected because two default-style branches would represent different portions of
one product and make it unclear which branch contains the authoritative repository.
Documentation must ship with the implementation it governs.

### Commit all work directly to `main`

Rejected for the planned production system because it removes the review and
integration boundary requested for this project.

