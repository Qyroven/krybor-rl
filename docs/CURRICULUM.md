# Curriculum

The curriculum is ordered by conceptual dependency, not by what looks most
impressive in a demo. Each stage produces reusable code and evidence.

| Stage | Core ideas | Required artifact | Status |
| --- | --- | --- | --- |
| 1. Foundations | agent/environment, reward, return, value, policy | vocabulary and problem formulation | Active |
| 2. Bandits | exploration, action values, incremental updates | epsilon-greedy comparison | Active |
| 3. Finite MDPs | Markov property, dynamics, returns, Bellman equations | validated stochastic GridWorld | Active |
| 4. Dynamic programming | evaluation, improvement, generalized policy iteration | DP algorithms agree on a small MDP | Active |
| 5. Monte Carlo | episodic returns, first/every visit, off-policy estimation | sampled estimates vs DP truth | Next |
| 6. Temporal difference | bootstrapping, SARSA, Q-learning, expected SARSA | cliff-walking comparison | Planned |
| 7. n-step methods | bias/variance horizon, n-step returns | controlled sweep over `n` | Planned |
| 8. Planning | model learning, Dyna, prioritized sweeping | planning-vs-interaction study | Planned |
| 9. Function approximation | features, SGD, generalization | linear value prediction | Planned |
| 10. Policy methods | policy gradient, baselines, actor-critic | variance and learning curves | Planned |
| 11. Deep RL | neural approximation, replay, target networks | minimal DQN-style baseline | Planned |
| 12. Advanced core | stability, offline/model-based/distributional topics | focused reproductions | Unscheduled |
| 13. Specialization | a chosen domain or research niche | capstone built on the core | Unscheduled |

## Immediate sequence

The existing Chapters 1–4 code is a reference baseline. Rebuild mastery in four
passes:

1. Complete the Chapter 1 vocabulary audit and formulate the GridWorld as an MDP.
2. Reconstruct epsilon-greedy and its incremental sample-average update.
3. Trace every GridWorld transition probability and reward by hand for one state.
4. Implement Bellman backups on paper, then verify policy and value iteration.

Only then open Chapter 5. The first Monte Carlo milestone should use the same
GridWorld so the only new variable is learning from sampled complete episodes.

## Choosing a specialization later

Do not reserve architecture for a niche before evidence points to one. Track which
questions keep pulling you back—sample efficiency, exploration, multi-agent
interaction, control, offline data, model learning, robustness, or another area.
Choose a specialization after the tabular and approximation foundations make its
tradeoffs legible.
