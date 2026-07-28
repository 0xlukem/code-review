# Contributing

Ground rules for proposing changes to homemade-review.

## Non-negotiables

1. **Never commit secrets.** No API keys, tokens, or credentials — ever. Workflows reference `${{ secrets.* }}` only. If a secret is accidentally committed, consider it compromised: revoke it immediately and rotate.
2. **The agent stays read-only.** `edit: deny` and the bash allowlist (`gh` + read-only `git`) are a security boundary, not a suggestion. PRs that loosen them need explicit justification.
3. **The reviewer advises, never gates.** Verdicts stay advisory (`SUGGEST CHANGES`), and the GitHub review event stays `COMMENT`. It never blocks merges and never modifies code.
4. **PR content is untrusted data.** Changes to the agent prompt must preserve the prompt-injection posture.

## Changing the rubric (`.opencode/agent/reviewer.md`, `rubrics/`)

The rubric is the product. Treat changes like code changes:

1. Open a PR with the rubric change.
2. **Let the PR review itself** — comment `/review` on it. A repo-local `reviewer.md` takes precedence, so your PR runs with *your modified rubric*: you taste the change before anyone merges it.
3. Ideally include before/after evidence in the PR description: what finding does the change catch or stop missing?

## Testing changes to workflows

- Test in this repo first (dogfooding PR), then in one external repo.
- Remember: `issue_comment` workflows run from the **default branch** — workflow changes only take effect after merging to `main`.
- After any user-facing workflow change, tag a new release (`vX`) so pinned callers can upgrade deliberately.

## Commit style

Short imperative messages describing the why: `rubric: raise cap to 30, never cut P0/P1`, `fix: persist git credentials for the action's git fetch`.

## Bugs and ideas

Open an issue with: what you expected, what happened, the Actions run log excerpt, and the PR link. For review-quality issues (missed findings, noise), paste the review section in question — rubric tuning is evidence-driven.
