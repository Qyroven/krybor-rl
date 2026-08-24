# Krybor RL product definition

Status: proposed  
Date: 2026-08-24

## Product statement

Krybor RL is an executable visual map of reinforcement learning. It connects
concepts, equations, implementations, experiments, applications, and guided
practice so a learner can move from intuition to evidence rather than merely read
or copy an algorithm.

The public product is a content-first interactive learning platform. The Python
package remains the mathematical and experimental engine beneath that product.
Infrastructure is a supporting engineering track used to operate the real system.

## Problem

Reinforcement learning is often learned through three disconnected artifacts:

- books explain mathematics but cannot expose dynamic behavior;
- notebooks demonstrate isolated algorithms but obscure relationships and reuse;
- courses impose an order but rarely preserve the learner's predictions, failures,
  tests, and experiments.

This fragmentation makes it possible to finish chapters without being able to
reconstruct an update rule, diagnose an implementation, or explain how one method
depends on another.

## Primary users

### Independent learner

A learner wants a trustworthy path through RL, interactive explanations, runnable
experiments, and an explicit mastery standard.

### Content author

An author wants one structured source for explanations, prerequisites, formulas,
code references, visualizations, exercises, and applications without hard-coding
the same relationship in several interfaces.

### Instructor — later phase

An instructor wants to compose paths and assignments, observe learner progress,
and assess evidence. Instructor accounts and cohort management are not part of V1.

## Core promise

A learner should be able to:

1. locate a concept in the RL knowledge graph;
2. see what knowledge it requires and what it unlocks;
3. understand its intuition and mathematical definition;
4. manipulate a visualization or simulation;
5. trace the mathematics into a tested implementation;
6. run a reproducible experiment;
7. complete an exercise that produces evidence of understanding;
8. connect the concept to algorithms and real applications.

## Product pillars

### Visual knowledge graph

RL is represented as typed relationships among concepts rather than only a linear
table of contents. Chapters and learning paths select routes through the graph;
they do not own duplicate copies of the concepts.

### Executable textbook

Important claims connect to code, tests, seeded experiment configurations, and
interactive demonstrations. Visualizations explain behavior; they do not replace
derivation or evidence.

### Guided mastery

Learning paths, exercises, assignments, and reflection prompts use the repository's
definition of done: concept, derivation, implementation, correctness, experiment,
and reflection.

### Applications map

Core RL concepts may connect to robotics, games, recommendation, operations
research, control, and other domains. Applications consume the RL core; they do
not redefine or distort it.

### Infrastructure as a real learning track

The platform is operated as a professional system. Containers, servers, networks,
cloud resources, observability, security, and orchestration are introduced in
response to real operational needs and preserved as code, diagrams, tests, and
runbooks.

## Product principles

- **RL remains the subject.** Infrastructure supports delivery and operation.
- **Content is the source of navigation.** The graph, paths, and related links are
  generated from structured content rather than duplicated in UI code.
- **Python is the source of mathematical truth.** Web code must not silently grow
  a second implementation of RL algorithms.
- **Evidence before completion.** Reading or running code alone does not establish
  mastery.
- **Complexity must be earned.** Accounts, databases, Kubernetes, distributed
  training, and AI services arrive only when a milestone needs them.
- **Accessible without an account.** Core knowledge remains publicly readable.
- **Reproducible by default.** Seeds, parameters, revisions, and assumptions are
  part of experiments and examples.
- **Operational changes are learning artifacts.** An infrastructure addition needs
  a rationale, validation, rollback, and runbook.

## North-star experience

A visitor lands on Krybor RL, selects a learning path or a node in the knowledge
map, studies a concept, manipulates its behavior, inspects the corresponding
Python implementation, predicts an experiment, runs it, and records evidence.
Later, the same content can be assigned by an instructor without being rewritten.

## Long-term product layers

```text
knowledge graph and structured content
                |
                v
visual textbook and interactive laboratories
                |
                v
learning paths, exercises, assignments, and progress
                |
                v
optional identity, cohorts, submissions, and instructor workflows
```

The first release stops before the final layer. See [V1 scope](V1_SCOPE.md).

## Success measures

V1 succeeds when a learner unfamiliar with the repository can complete the
Chapter 1 foundations path without live guidance and can accurately explain the
agent-environment boundary, reward versus return, policy versus value, the Markov
property, and the effect of one reward-design change.

Engineering success additionally requires:

- content relationships are validated automatically;
- the visual experience links to the authoritative Python implementation;
- the complete local system starts through one documented command;
- CI tests the content, Python engine, web application, and their integration;
- a new concept can be added without modifying hard-coded navigation.

## Non-goals

Krybor RL is not intended to be:

- a replacement for Sutton and Barto or other primary references;
- a generic learning-management system;
- a collection of unrelated notebooks;
- an infrastructure demo with no product need;
- an algorithm benchmark leaderboard without educational context;
- a robotics framework whose architecture constrains the RL core.

