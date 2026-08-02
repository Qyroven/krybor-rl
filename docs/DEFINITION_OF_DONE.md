# Definition of done

A topic is not done because its code executes or because the corresponding book
chapter has been read. Mark it complete only when all six layers are present.

## Topic checklist

- [ ] **Concept:** explain the problem, assumptions, objective, and update rule in
      your own words.
- [ ] **Derivation:** connect every term in the equation to a variable or operation
      in code.
- [ ] **Implementation:** write or reconstruct the smallest clear version without
      hiding the core update in a library.
- [ ] **Correctness:** test a hand-computable case, boundary conditions, and at
      least one mathematical invariant.
- [ ] **Experiment:** save seeds and hyperparameters, compare against a meaningful
      baseline, and report aggregate metrics where randomness matters.
- [ ] **Reflection:** record the prediction, result, surprise, failure mode, and next
      question.

## Promotion checklist for `src/`

- [ ] The code has one clear responsibility and belongs to the documented package.
- [ ] Environment logic and algorithm logic remain separate.
- [ ] Public inputs are validated and names reflect the mathematics.
- [ ] Tests fail when the central update is intentionally broken.
- [ ] A runnable command or config demonstrates the behavior.
- [ ] `make check` passes.

## Mastery check

You should be able to answer without opening the implementation:

1. What information does the method assume is available?
2. Is its update expected, sampled, bootstrapped, or some combination?
3. What quantity is estimated and what is the target?
4. Which hyperparameters change the fixed point, and which only change the path?
5. Name a case where the method fails or becomes impractical.

If one answer is vague, the topic is still active—and that is useful information,
not a failure.
