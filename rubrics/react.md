# React rubric overlay

Apply in addition to the base rubric when the PR touches React code.

## P0/P1 candidates

- Missing or wrong dependencies in `useEffect` / `useMemo` / `useCallback` causing stale closures or infinite loops
- State updates after unmount (async handlers without cleanup)
- Derived state stored in `useState` instead of computed during render
- Conditional hook calls
- Direct DOM manipulation that fights React's rendering

## P2 candidates

- Unnecessary re-renders: unstable object/array props, missing memoization in hot paths
- Missing `key`, or array index as `key` on dynamic lists
- Effects that should be event handlers
- Prop drilling deeper than 2 levels where composition would do

## P3 candidates

- Naming consistency for handlers (`handleX` vs `onX`), matching the repo's convention

Always: check a11y on new JSX — labels on inputs, `alt` on images, keyboard operability of custom widgets.
