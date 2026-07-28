# homemade-review

A personal, self-hosted AI code reviewer built on [OpenCode](https://opencode.ai). Comment `/review` on any pull request and it posts a structured **P0–P3 review** — inline on the exact diff lines for the serious stuff, with one-click fix suggestions and explicit trade-offs — aware of your repo's own rules.

Built around five ideas:

1. **Customizable rubrics** — the default P0–P3 rubric is the baseline. Drop a `.github/reviewer.md` in your repo to override it, or add per-stack overlays in `rubrics/`.
2. **It knows your rules** — it reads your repo's `AGENTS.md` before judging anything.
3. **Explicit trade-offs** — every finding explains what the code does, what it costs, and what the alternative costs.
4. **Inline where it matters** — P0/P1 findings land on the exact diff line, with GitHub `suggestion` blocks (one-click "Apply suggestion") when the fix is expressible in code.
5. **Explanation levels** — `beginner` learns what the bug class is and why the fix works, `medium` gets the compact review, `advanced` gets just the radar. Configurable per repo and per invocation.

## How it works

```
you comment "/review" on a PR in any of your repos
        │
        ▼
that repo's tiny caller workflow
        │
        ▼
reusable workflow in THIS repo  (.github/workflows/reusable-review.yml)
  - gated to OWNER/MEMBER/COLLABORATOR comments only
  - checks out the PR code
  - fetches the latest reviewer agent + rubrics from this repo
        │
        ▼
OpenCode runs the reviewer  (.opencode/agent/reviewer.md)
  - reads AGENTS.md + custom rubric + stack overlays
  - analyzes the diff with the P0-P3 rubric
        │
        ▼
posts ONE GitHub Review: summary body + inline comments for P0/P1
(falls back to a plain comment if the review API rejects the payload)
```

Update the rubric once in this repo — every connected repo picks it up on the next `/review`.

## Install (2 steps)

1. **Copy [`templates/review.yml`](templates/review.yml)** to `.github/workflows/review.yml` in your repo.
2. **Add your OpenCode API key** as a repository secret named `OPENCODE_API_KEY`
   (create one at [opencode.ai/auth](https://opencode.ai/auth) → Create API Key; add it under
   repo **Settings → Secrets and variables → Actions → New repository secret**).
   One key covers both OpenCode plans: **Go** (subscription, `opencode-go/...` models) and **Zen** (pay-as-you-go, `opencode/...` models).

Then comment `/review` on any pull request.

> **Visibility:** cross-repo installs require this repo to be **public** (the agent fetch is unauthenticated). While it stays private, the workflow only works inside this repo itself — a repo-local `reviewer.md` always takes precedence over the central one, which also enables fully vendored installs.
>
> Alternative: if you don't want to depend on this repo, you can still vendor everything — copy `.opencode/agent/reviewer.md`, `rubrics/`, and a standalone workflow into your repo. You lose auto-updates.

## Usage

| Action | How |
|---|---|
| Standard review | Comment `/review` |
| Focus hint | `/review focus on security` or `/review only the auth changes` |
| Change level once | `/review level:beginner` (overrides repo config) |
| Force a fresh full review | `/review full` (skips the delta shortcut, even without new commits) |
| Delta review | Push fixes, comment `/review` again — it acknowledges what you fixed and reports only what's still open |

## Configure

| What | How | Default |
|---|---|---|
| Model | `with: model:` in the caller workflow, or repo variable `REVIEWER_MODEL` | `opencode-go/deepseek-v4-flash` |
| Explanation level | `with: explanation_level:`, repo variable `REVIEWER_LEVEL`, or `/review level:x` per invocation | `medium` |
| Custom rubric | Add `.github/reviewer.md` to the reviewed repo | built-in rubric |
| Per-stack overlays | `rubrics/<stack>.md` (shipped: `react.md`, `vue.md`, `python.md`) | auto-detected |
| Repo conventions | The reviewer reads the repo's `AGENTS.md` automatically | — |

## Severity ladder

| Level | Meaning | Where it appears |
|---|---|---|
| **P0** | Blocks merge (broken behavior, XSS/injection, exposed secrets, data loss) | **Inline** on the diff line + summary |
| **P1** | Should fix (edge-case bugs, missing error handling, race conditions, broken types) | **Inline** + summary |
| **P2** | Suggestion (structure, performance that matters, weak typing, missing tests) | Summary only |
| **P3** | Nit (style beyond what tooling enforces) | Summary only |

Anti-noise by design: "when in doubt, don't report", a 30-finding ceiling that cuts P3s and P2s first — never a P0/P1 — and it never repeats what your linter already catches.

## Explanation levels

| Level | Each finding includes |
|---|---|
| `beginner` | Full finding + **Learn corner**: what this bug class is, how it fails or gets exploited in the real world, why the fix works |
| `medium` | What + why it matters + trade-off (the default) |
| `advanced` | Flag, location, minimal fix hint. No trade-offs, no teaching |

## Dependency security

Changes to manifests/lockfiles (`package.json`, `requirements.txt`, `go.mod`, ...) are always reviewed as P0/P1 candidates: typosquatting, pinned versions with known CVEs (a pin is not proof of safety), new `preinstall`/`install`/`postinstall` scripts, license and maintenance signals, and live registry verification for obscure packages when web access is available. It detects *suspicious signals* — it complements, not replaces, dedicated scanners (Socket, Snyk, Dependabot).

## Security notes

- **Your API key is never in the repo** — public or private. It lives in GitHub's encrypted secrets store; workflows only contain the `${{ secrets.OPENCODE_API_KEY }}` reference, and GitHub masks it in logs. This central repo contains **zero** secrets: every installer uses their own key, from their own repo.
- The workflow only runs for comments by **OWNER, MEMBER, or COLLABORATOR** — strangers can't spend your credits.
- The `GITHUB_TOKEN` is least-privilege (read code, write PR reviews) and expires with the job.
- The agent has **no edit permissions** and a restricted bash allowlist (`gh` + read-only `git`).
- The agent treats PR content as **untrusted data** to reduce prompt-injection risk.
- **Supply chain:** your repos call this repo's reusable workflow. Pin `@v1` (standard) or a full commit SHA (maximum security). Protect `main` here (branch protection + required reviews), since every connected repo trusts it.
- Still: treat the output as advice, not ground truth. It is a reviewer, not a gate.

## Cost

| Plan | Prefix | Cost per review |
|---|---|---|
| **OpenCode Go** (subscription) | `opencode-go/...` | ~$0 marginal — flat plan, 20+ open models (Kimi K3/K2.6, DeepSeek V4, Qwen 3.7, GLM 5.2, Grok 4.5, ...) |
| **OpenCode Zen** (pay-as-you-go) | `opencode/...` | From fractions of a cent (`deepseek-v4-flash`) up to ~$0.05–0.20 for top models |

## Roadmap

- ~~inline comments on diff lines~~ ✅ (P0/P1, with `suggestion` blocks)
- ~~centralized reusable workflow~~ ✅
- ~~explanation levels~~ ✅
- **v0.3** — chunked reviews for PRs over ~1500 lines (batched per-file analysis, merged), optional auto-trigger on PR open
- **v0.4** — OSV API integration for exact-version CVE checks, eval harness scoring the reviewer against real PRs
