# Documentation map

Krybor RL has three connected concerns: reinforcement-learning knowledge, the
interactive learning product, and the infrastructure that operates that product.
This index identifies the authoritative document for each concern.

## Product

- [Product definition](product/PRODUCT.md) defines the users, problem, promise,
  principles, and long-term direction.
- [Version 1 scope](product/V1_SCOPE.md) is the binding feature boundary for the
  first public interactive release.
- [Content model](product/CONTENT_MODEL.md) defines the source format for concepts,
  relationships, learning paths, exercises, and assignments.

## Architecture

- [System architecture](architecture/SYSTEM.md) defines the target platform
  boundaries and dependency rules.
- [Current RL architecture](ARCHITECTURE.md) documents the implemented Python
  packages and their responsibilities.
- [Architecture decision records](architecture/adr/README.md) preserve decisions
  whose rationale should survive individual implementations.

## Learning and operations

- [RL curriculum](CURRICULUM.md) defines the conceptual learning sequence.
- [Definition of done](DEFINITION_OF_DONE.md) defines evidence required before an
  RL topic is considered complete.
- [Infrastructure roadmap](infrastructure/ROADMAP.md) turns operation of Krybor RL
  into a second, supporting learning track.
- [Vision](VISION.md) summarizes how the current repository grows into the target
  product.

## Authority

When documents disagree, use this order:

1. accepted architecture decision records;
2. `product/V1_SCOPE.md` for the current product boundary;
3. `architecture/SYSTEM.md` for system boundaries;
4. the roadmap documents for sequencing;
5. README files as summaries.

