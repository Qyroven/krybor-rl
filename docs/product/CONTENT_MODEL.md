# Content model

Status: proposed  
Date: 2026-08-24

## Purpose

Structured content is the source of truth for the visual textbook, knowledge
graph, related links, learning paths, exercises, and assignments. UI components
render that source; they do not own a second copy of the relationships.

## Storage model

The planned content tree is:

```text
content/
├── concepts/
├── algorithms/
├── applications/
└── glossary/

learning/
├── paths/
├── exercises/
├── assignments/
└── rubrics/
```

Narrative pages use MDX with validated front matter. Learning compositions use
YAML when they do not need narrative bodies. The concrete schema implementation
will be selected with the web framework, but the semantic fields below are stable.

## Concept identity

Every entity has a permanent, lowercase, hyphenated `id`. File names should match
the ID. Display titles may change without breaking relationships; IDs should not
change after publication without an explicit migration.

Example:

```yaml
id: reward
kind: concept
title: Reward
summary: A scalar signal that defines the agent's immediate objective feedback.
status: draft
prerequisites: []
related:
  - return
  - objective
unlocks:
  - reward-design
implementations:
  - path: src/krybor_rl/environments/gridworld.py
    symbol: GridWorld._move
visualizations:
  - agent-environment-loop
exercises:
  - ch01-reward-design
applications:
  - robot-navigation
references:
  - id: sutton-barto-2018
    locator: section 1.3
mastery:
  - distinguish reward from return
  - explain how reward design can miss the designer's intention
```

## Required concept fields

| Field | Meaning |
| --- | --- |
| `id` | Stable graph identifier |
| `kind` | `concept`, `algorithm`, `application`, or `glossary` |
| `title` | Human-readable title |
| `summary` | One-sentence description used in navigation |
| `status` | `draft`, `review`, or `published` |
| `prerequisites` | Concepts required before this entity |
| `related` | Non-prerequisite conceptual relationships |
| `mastery` | Observable claims a learner should demonstrate |

Optional typed connections include implementations, visualizations, exercises,
applications, references, and concepts unlocked by this entity.

## Narrative anatomy

Concept and algorithm pages use these semantic sections when applicable:

1. intuition;
2. definition and assumptions;
3. notation and formula;
4. derivation;
5. worked example;
6. interactive visualization or simulation;
7. implementation mapping;
8. correctness evidence;
9. applications;
10. common mistakes and failure modes;
11. exercises and mastery check;
12. related concepts and references.

Not every concept needs a formula or algorithm implementation. A missing section
is acceptable when it is conceptually irrelevant, not when content is unfinished.

## Relationship rules

- `prerequisites` must form a directed acyclic graph for each supported learning
  path unless a documented exception represents mutually developed concepts.
- every referenced ID must exist;
- an entity must not list itself;
- duplicate relationships are invalid;
- `related` is not a substitute for a prerequisite;
- chapter membership belongs to a learning path, not the concept identity;
- application nodes point back to the core concepts and algorithms they consume;
- source references must identify a stable work and locator.

## Learning paths

A learning path is an ordered traversal over existing entities:

```yaml
id: foundations
title: RL Foundations
summary: Build a precise agent-environment mental model.
audience: beginning RL learner
outcomes:
  - formulate a task as an agent-environment interaction
  - distinguish reward, return, policy, and value
steps:
  - type: concept
    id: agent
  - type: concept
    id: environment
  - type: visualization
    id: agent-environment-loop
  - type: assignment
    id: ch01-reward-design
```

Paths may impose a pedagogical order but must not duplicate concept bodies.

## Exercises and assignments

An exercise checks one focused outcome. An assignment composes concepts,
predictions, implementation or interaction, evidence, and reflection.

```yaml
id: ch01-reward-design
title: Reward design in the rescue GridWorld
concepts:
  - reward
  - objective
  - return
tasks:
  - record a prediction before changing a parameter
  - change exactly one reward
  - solve and compare the resulting policy
  - explain whether objective or dynamics changed
evidence:
  - prediction
  - parameter diff
  - policy comparison
  - written explanation
rubric:
  - distinguishes reward mechanics from transition dynamics
  - connects the observation to expected return
```

V1 completion is stored locally as completion state, not as a graded server-side
submission.

## Implementation references

Content points to the authoritative source file and, when useful, a public symbol.
Line numbers must not be stored because ordinary edits make them stale. The web
renderer may resolve source links to the current repository revision.

## Formula and notation rules

- notation is defined before use;
- symbols use consistent names across related pages;
- formulas are accompanied by a plain-language interpretation;
- important equations connect each term to implementation variables or operations;
- copied prose and excessive quotation are prohibited;
- source citations distinguish original explanation from referenced definitions.

## Validation

CI must eventually reject:

- malformed front matter;
- unknown or duplicate IDs;
- broken relationships and source paths;
- prerequisite cycles;
- invalid learning-path steps;
- assignments whose concepts do not exist;
- published entities missing required narrative sections or mastery criteria.

## Authoring workflow

```text
question
→ identify or create graph nodes
→ write relationships and mastery outcomes
→ author narrative and evidence
→ add visualization or exercise only when it clarifies the concept
→ validate schema and links
→ review mathematical and pedagogical correctness
→ publish through the normal branch and PR workflow
```

