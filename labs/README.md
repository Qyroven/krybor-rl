# Labs

Labs preserve the learning sequence. They are chapter-shaped because their job is
to make concepts visible; reusable implementation is promoted into `src/` after
it satisfies the repository's definition of done.

## Active track

| Lab | Focus | Exit evidence |
| --- | --- | --- |
| [Chapter 1](ch01_foundations/README.md) | RL vocabulary and problem formulation | a precise agent-environment loop |
| [Chapter 2](ch02_bandits/README.md) | exploration and incremental action values | seeded epsilon comparison |
| [Chapter 3](ch03_finite_mdp/README.md) | dynamics, returns, value functions | validated GridWorld model |
| [Chapter 4](ch04_dynamic_programming/README.md) | expected Bellman backups | two control methods agree |

## Lab convention

Each lab should eventually contain:

```text
README.md       concepts, derivation, questions, completion checklist
exercise_*.py   small reconstructions when code is useful
```

Do not put a second production implementation in a lab. Use exercises to reveal
an idea, then promote the clean form to `src/krybor_rl/` and test it there.
