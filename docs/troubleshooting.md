# Troubleshooting

Every failure below was hit while building this project. Symptom → cause → fix.

## The workflow never runs when I comment `/review`

Check in order:

1. **Actions are enabled**: repo Settings → Actions → General → allow actions.
2. **The comment is on a PR**, not an issue, and contains `/review` in the body.
3. **You are OWNER, MEMBER, or COLLABORATOR** — the security gate ignores everyone else (by design; strangers must not spend your API credits).
4. **The workflow file exists on the default branch** — `issue_comment` workflows run from the default branch's version of the file, not the PR branch's.

## `fatal: could not read Username for 'https://github.com': No such device or address`

**Cause:** the checkout step had `persist-credentials: false`, so the opencode action had no git credentials to `git fetch` the PR branch.

**Fix:** remove `persist-credentials: false` (keep the default `true`). The token is least-privilege and ephemeral; the agent is read-only.

## `The nested job ... is requesting 'issues: write, pull-requests: write, id-token: write', but is only allowed '...: none'`

**Cause:** GitHub zeroes all permissions when a caller job invokes a reusable workflow without declaring them. The caller is the trust boundary.

**Fix:** declare the permissions block in the caller job (already present in `templates/review.yml`):

```yaml
permissions:
  id-token: write
  contents: read
  pull-requests: write
  issues: write
```

## The run fails immediately with a model/provider auth error

**Cause:** missing or misnamed API-key secret.

**Fix:** the secret must be named exactly `OPENCODE_API_KEY` (repo Settings → Secrets and variables → Actions) and contain a valid key from [opencode.ai/auth](https://opencode.ai/auth). Secrets are write-only — if unsure, replace it.

## The review posts as one plain comment, no inline comments

**That's the fallback working as designed** — the review API rejected the inline payload (usually an HTTP 422 from a line number that's not in the diff, common after force-pushes) and the reviewer posted the summary instead of losing the review.

**Check:** the summary ends with a note that inline comments were skipped, and the Actions run log shows the failed POST. Usually transient; re-comment `/review full`.

## "No new commits since prior review" but I want a fresh review

**By design:** identical re-runs get a compact no-change note.

**Fix:** comment `/review full` (or add any new parameter, e.g. `level:beginner`) — new parameters force a full fresh review.

## Inline comments appear but without "Apply suggestion" buttons

The reviewer only emits `suggestion` blocks for fixes touching 1–3 lines (architectural or multi-file fixes get flags only — by design). If a clear 1-line fix lacks a suggestion, that's a known model-fidelity issue we're tuning: smaller models sometimes drop the nested code fence. Try `/review full`, or a stronger model (`REVIEWER_MODEL=opencode-go/kimi-k3`).

## Cross-repo install: the "Fetch the reviewer agent" step fails with 404

**Cause:** the central repo is private — the agent fetch from `raw.githubusercontent.com` is unauthenticated.

**Fix:** make the central repo public, or vendor the files (copy `.opencode/agent/reviewer.md` into the target repo — a repo-local agent always takes precedence).

## The review posts, then a `github-actions Bot` comment appears: "Author identity unknown"

**Cause:** some part of the OpenCode action (or a post-run step) invoked git, but the runner had no `user.name` / `user.email` configured. Git fails with `fatal: empty ident name ... not allowed` and the error ends up as a PR comment.

**Fix:** configure git identity in the reusable workflow before running the agent (already present in `reusable-review.yml`):

```yaml
- name: Configure git identity
  run: |
    git config --global user.name "github-actions[bot]"
    git config --global user.email "github-actions[bot]@users.noreply.github.com"
```

Remember that callers pin `@v1`; after merging the fix you must move the `v1` tag so installs pick it up.

## The review ignored the repo's conventions

**Check:** does `AGENTS.md` exist at the repo root? The reviewer reads it before judging. If it exists and was ignored, add explicit pointers in `.github/reviewer.md` (the custom-rubric override).
