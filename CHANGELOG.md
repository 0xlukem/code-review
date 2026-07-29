# Changelog

Notable changes to homemade-review, loosely following [Keep a Changelog](https://keepachangelog.com/).

## [0.2.0] — 2026-07-28

The "real reviewer" release: inline reviews, explanation levels, delta mode, and centralization — every feature validated on live demo PRs.

### Added

- **Inline P0/P1 comments** posted as a single GitHub Review, with `suggestion` blocks (batch-applicable "Apply suggestion" buttons) for fixes touching 1–3 lines, and a mandatory fallback to a plain summary comment if the review API rejects the payload
- **Explanation levels** — `beginner` (mandatory 5-part Learn corner per finding: analogy, exploit scenario, try-it-yourself payload, why the fix works, concept to explore), `medium` (compact, decision-focused), `advanced` (radar only). Set per repo (input or `REVIEWER_LEVEL` variable) or per invocation (`/review level:x`)
- **Delta reviews** — re-reviews acknowledge fixed findings in "Resolved since last review" and report only what's still open; carried-over findings link to the original inline thread, never re-posted
- **Centralized reusable workflow** — caller repos install a ~15-line workflow; agent and rubrics are fetched from the central repo at runtime; a repo-local `reviewer.md` always takes precedence (vendored installs, rubric PRs self-review)
- **Output contract** — a pre-post checklist the reviewer must satisfy (verdict/scope/level lines, footer, suggestions on 1–3-line fixes, severity calibration, dependency-manifest coverage, Learn corner at beginner)
- **Dependency security rules** — typosquatting, pinned versions with known CVEs ("a pin is not proof of safety"), `pre/postinstall` scripts as P0 suspects, registry verification for obscure packages, unused-dependency detection
- **Advisory verdicts** (`SUGGEST CHANGES`) — the GitHub review event is always `COMMENT`; the bot advises, never blocks
- **Docs** — `docs/usage.md`, `docs/troubleshooting.md` (every real failure hit during development), `CONTRIBUTING.md`, and a measured cost table
- **CI hardening** — caller-granted permissions model, `OPENCODE_CONFIG_CONTENT` denying `external_directory`, `timeout-minutes: 15`

### Changed

- **Default model**: `deepseek-v4-flash` → `minimax-m3`, chosen by A/B test on real PRs (full format fidelity vs dropped structure; $0.038 vs $0.005 per small-PR review — both trivially cheap)
- Findings cap raised 10 → 30, cutting P3s and P2s first — never a P0/P1
- `medium` level made deliberately terser to widen the gap with `beginner`

### Fixed

- Git credential failure: `persist-credentials: false` broke the action's `git fetch` of the PR branch
- Caller jobs silently receiving zero permissions (GitHub zeroes undeclared permissions on `workflow_call`)
- Headless hang: the agent writing its review payload to `/tmp` triggered an `external_directory` "ask" with no human to answer in CI
- A P1 (known CVE in a pinned dependency) silently dropped by the 10-finding cap
- Delta shortcut blocking fresh full reviews without new commits — `/review full` added
- Off-diff fixes (e.g. missing imports) getting no suggestion: in-function import fallback added

## [0.1.0] — 2026-07-24

First working version: comment `/review` on a PR, get one structured P0–P3 summary comment.

### Added

- `reviewer` agent: P0–P3 severity rubric, anti-noise rules ("when in doubt, don't report"), explicit trade-off per finding, prompt-injection posture, read-only permissions
- Per-stack rubric overlays (`rubrics/react.md`, `vue.md`, `python.md`) and `AGENTS.md` awareness
- Mention-triggered workflow gated to OWNER/MEMBER/COLLABORATOR comments
- Dependency-file review (typosquatting, pinning, licenses)
- Re-review continuity (reads its previous review before re-reviewing)
