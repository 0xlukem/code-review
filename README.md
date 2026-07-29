# homemade-review

A personal, self-hosted AI code reviewer built on [OpenCode](https://opencode.ai). Comment `/review` on any pull request and it posts a structured **P0–P3 review** — inline on the exact diff lines for the serious findings, with one-click fix suggestions and explicit trade-offs — aware of your repo's own rules.

Built around five ideas:

1. **Customizable rubrics** — the default P0–P3 rubric is the baseline. Drop a `.github/reviewer.md` in your repo to override it, or add per-stack overlays in `rubrics/`.
2. **It knows your rules** — it reads your repo's `AGENTS.md` before judging anything.
3. **Explicit trade-offs** — every finding explains what the code does, what it costs, and what the alternative costs.
4. **Inline where it matters** — P0/P1 findings land on the exact diff line, with GitHub `suggestion` blocks (batch-applicable, one-click fixes) when the fix is expressible in code.
5. **Explanation levels** — `beginner` learns what the bug class is and why the fix works, `medium` gets the compact review, `advanced` gets just the radar.

## How it works

```
you comment "/review" on a PR in any of your repos
        │
        ▼
that repo's tiny caller workflow  (templates/review.yml)
        │
        ▼
reusable workflow in THIS repo  (.github/workflows/reusable-review.yml)
  - gated to OWNER/MEMBER/COLLABORATOR comments only
  - checks out the PR code
  - fetches the latest reviewer agent + rubrics from this repo
    (a repo-local reviewer.md always wins)
        │
        ▼
OpenCode runs the reviewer  (.opencode/agent/reviewer.md)
        │
        ▼
posts ONE GitHub Review: summary body + inline comments for P0/P1
(falls back to a plain comment if the review API rejects the payload)
```

Update the rubric once in this repo — every connected repo picks it up on the next `/review`.

## Quickstart

1. Copy [`templates/review.yml`](templates/review.yml) to `.github/workflows/review.yml` in your repo.
2. Add your OpenCode API key as a repository secret named `OPENCODE_API_KEY`
   ([opencode.ai/auth](https://opencode.ai/auth) → Create API Key; repo **Settings → Secrets and variables → Actions**).
3. Comment `/review` on any pull request.

Full command reference, config options, and overrides: **[docs/usage.md](docs/usage.md)**.

## Costs

Measured on real PRs with both candidate models (small PR, +~40 lines). The default was chosen by A/B test, not vibes:

| Model | Agent calls | Tokens (in / out) | Cost | Format fidelity |
|---|---|---|---|---|
| `deepseek-v4-flash` | 14 | ~160k / ~7.4k | $0.005 | Finds the bugs, drops the structure |
| `minimax-m3` **(default)** | 22 | ~350k / ~8.6k | $0.038 | Full output contract (suggestions, levels, verdicts) |

Both are trivially cheap; correctness and format discipline won. `deepseek-v4-flash` remains available as the ultra-budget option via `REVIEWER_MODEL`.

| PR size | Lines changed | Est. tokens (in / out) | deepseek-v4-flash (PAYG) | OpenCode Go |
|---|---|---|---|---|
| Small | < 200 | ~150–250k / 5–10k | **≤ $0.01** (measured: $0.005) | $0 |
| Medium | 200–800 | ~400–700k / 10–20k | ~$0.01–0.02 | $0 |
| Large | 800–1,500 | ~0.7–1.2M / 15–30k | ~$0.02–0.05 | $0 |
| XL | > 1,500 (triage mode) | 1M+ / 20–40k | ~$0.05–0.10 | $0 |

Estimates extrapolated from the measured small-PR run; Zen's prompt caching pushes real costs below list price. Higher-end models (Kimi K3, Claude Sonnet 5) multiply cost roughly 7–30x.

## Security

- **Your API key is never in the repo** — public or private. It lives in GitHub's encrypted secrets store; workflows only reference it. This central repo contains zero secrets.
- Workflow runs only for **OWNER/MEMBER/COLLABORATOR** comments — strangers can't spend your credits.
- `GITHUB_TOKEN` is least-privilege (read code, write PR reviews) and expires with the job. Caller jobs must explicitly grant every permission — a compromised reusable workflow can't escalate beyond what callers allow.
- The agent is **read-only** (`edit: deny`, bash allowlist: `gh` + read-only `git`) and treats PR content as untrusted data.
- Pin the reusable workflow by tag (`@v1`) or full SHA for maximum supply-chain safety. Protect `main` here — every connected repo trusts it.
- The reviewer **advises** (verdicts like `SUGGEST CHANGES`, review event always `COMMENT`). It never blocks, never modifies code.

## Docs

| Doc | Contents |
|---|---|
| [docs/usage.md](docs/usage.md) | All `/review` commands, levels, per-repo config, custom rubrics |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Every failure we hit building this, and its fix |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Ground rules for proposing changes |
| [CHANGELOG.md](CHANGELOG.md) | What shipped, when, and what it fixed |

## Roadmap

- **next** — `show_cost` flag (default off): appends the review's token/cost line to the summary
- **v0.3** — chunked reviews for PRs over ~1500 lines, optional auto-trigger on PR open
- **v0.4** — OSV API for exact-version CVE checks, eval harness scoring the reviewer against real PRs
