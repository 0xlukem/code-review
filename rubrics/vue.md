# Vue rubric overlay

Apply in addition to the base rubric when the PR touches Vue code.

## P0/P1 candidates

- Mutating props directly
- Side effects in `computed` properties
- Missing cleanup in watchers or lifecycle hooks (timers, listeners, subscriptions)
- Reactivity loss: destructuring reactive objects without `toRefs`, or replacing a whole `reactive()` object
- `v-html` with unsanitized user content (XSS)

## P2 candidates

- `v-if` and `v-for` on the same element
- Missing `:key`, or index-as-key in `v-for`
- Watchers that should be computed properties
- Single-file components mixing unrelated concerns

## P3 candidates

- Options API vs Composition API consistency with the rest of the repo
- Naming consistency for emits and props
