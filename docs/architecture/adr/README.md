# Architecture decision records

Architecture decision records explain decisions that affect several parts of the
system or are expensive to reverse. They preserve context and trade-offs rather
than merely announcing the chosen tool.

## Status lifecycle

```text
proposed → accepted → superseded
                   ↘ rejected
```

An accepted ADR is immutable apart from corrections and status changes. A new ADR
supersedes a decision when the context changes.

## Index

- [ADR 0001 — Use a polyglot monorepo](0001-use-a-polyglot-monorepo.md)
- [ADR 0002 — Keep the RL engine independent](0002-keep-the-rl-engine-independent.md)
- [ADR 0003 — Use main, develop, and short-lived branches](0003-use-main-develop-and-short-lived-branches.md)
- [ADR 0004 — Defer identity and RBAC until V2](0004-defer-identity-and-rbac-until-v2.md)

