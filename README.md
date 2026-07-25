# homemade-review

A personal, self-hosted AI code reviewer built on [OpenCode](https://opencode.ai). Comment `/review` on any pull request and it posts a structured **P0–P3 review** with explicit trade-offs — aware of your repo's own rules.

Unlike generic review bots, it is built around three ideas:

1. **Customizable rubrics** — the default P0–P3 rubric is just the baseline. Drop a `.github/reviewer.md` in your repo to override it, or add per-stack overlays in `rubrics/`.
2. **It knows your rules** — it reads your repo's `AGENTS.md` before judging anything, so it reviews against *your* conventions, not generic ones.
3. **Explicit trade-offs** — every finding explains what the code does, what it costs, and what the alternative costs. No bare "this is wrong" comments.

## How it works

```
you comment "/review" on a PR
        │
        ▼
GitHub Actions workflow  (.github/workflows/review.yml)
  - gated to OWNER/MEMBER/COLLABORATOR comments only
  - checks out the PR code
        │
        ▼
OpenCode runs the reviewer agent  (.opencode/agent/reviewer.md)
  - reads AGENTS.md + custom rubric + stack overlays
  - analyzes the diff with the P0-P3 rubric
        │
        ▼
posts exactly one review comment on the PR
```

## Install (3 steps)

1. **Copy the files** into your repo: `.opencode/agent/reviewer.md`, `.github/workflows/review.yml`, and (optionally) `rubrics/`.
2. **Add your OpenCode API key** as a repository secret named `OPENCODE_API_KEY`
   (create one at [opencode.ai/auth](https://opencode.ai/auth) → Create API Key; add it under
   repo **Settings → Secrets and variables → Actions → New repository secret**).
   One key covers both OpenCode plans: **Go** (subscription, `opencode-go/...` models) and **Zen** (pay-as-you-go, `opencode/...` models).
3. **Comment `/review`** on any pull request.

Usage extras:

- **Focus hints:** `/review focus on security` or `/review only the auth changes`
- **Delta reviews:** push fixes, comment `/review` again — it reads its previous review, acknowledges what you fixed, and only reports what's new
- **Dependency awareness:** changes to manifests/lockfiles (`package.json`, `requirements.txt`, ...) are always reviewed as P0/P1 candidates (supply-chain risk, pinning, licenses)

No GitHub App installation required — it uses the runner's built-in `GITHUB_TOKEN`.

## Configure

| What | How |
|---|---|
| Model | Set a repository **variable** `REVIEWER_MODEL` (Settings → Secrets and variables → Actions → Variables). Default: `opencode-go/deepseek-v4-flash` (Go subscription). Examples: `opencode-go/kimi-k3` (Go, higher quality), `opencode/claude-sonnet-5` (Zen pay-as-you-go), `anthropic/claude-sonnet-4-6` (your own Anthropic key — needs an `ANTHROPIC_API_KEY` secret instead) |
| Custom rubric | Add `.github/reviewer.md` to the reviewed repo — it overrides the default rubric |
| Per-stack overlays | Add `rubrics/<stack>.md` (shipped: `react.md`, `vue.md`, `python.md`) |
| Repo conventions | The reviewer reads the repo's `AGENTS.md` automatically |

## Severity ladder

| Level | Meaning | Examples |
|---|---|---|
| **P0** | Blocks merge | Broken behavior, XSS/injection, exposed secrets, data loss |
| **P1** | Should fix | Edge-case bugs, missing error handling, race conditions, broken types |
| **P2** | Suggestion | Structure, performance that matters, weak typing, missing tests |
| **P3** | Nit | Style and naming beyond what tooling enforces |

Anti-noise by design: "when in doubt, don't report", it never repeats what your linter already catches, and a 30-finding ceiling that cuts P3s and P2s first — never a P0/P1 (tunable per repo via `.github/reviewer.md`).

## Security notes

- The workflow only runs for comments by **OWNER, MEMBER, or COLLABORATOR** — strangers can't spend your API credits.
- The `GITHUB_TOKEN` is least-privilege: read code, write PR comments. Nothing else.
- The agent has **no edit permissions**; it can only read and comment.
- The agent treats PR content as untrusted data to reduce prompt-injection risk.
- Still, treat its output as advice, not ground truth. It is a reviewer, not a gate.

## Cost

Two ways to pay, same `OPENCODE_API_KEY`:

| Plan | Prefix | Cost per review |
|---|---|---|
| **OpenCode Go** (subscription) | `opencode-go/...` | ~$0 marginal — flat monthly plan, 22 open models (Kimi K3/K2.6, DeepSeek V4, Qwen 3.7, GLM 5.2, Grok 4.5, ...) |
| **OpenCode Zen** (pay-as-you-go) | `opencode/...` | From fractions of a cent (`deepseek-v4-flash`) up to ~$0.05–0.20 for top models (Claude Sonnet 5, GPT-5.6) |

The default (`opencode-go/deepseek-v4-flash`) keeps reviews effectively free if you have a Go subscription.

## Roadmap

- **v0.2** — inline review comments on exact diff lines (GitHub Reviews API), with summary fallback
- **v0.3** — optional auto-trigger on PR open/update, per-repo config file
- **v1.0** — example reviews, one-command installer
