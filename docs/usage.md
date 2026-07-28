# Usage

Everything you can do with homemade-review, from the daily flow to per-repo customization.

## The `/review` command

Comment on any pull request:

| Command | What it does |
|---|---|
| `/review` | Standard review: one GitHub Review — summary + inline comments for P0/P1 |
| `/review focus on security` | Focus hint: steers the analysis toward an area (free text after `/review`) |
| `/review level:beginner` | One-off explanation-level override (`beginner` / `medium` / `advanced`) |
| `/review full` | Forces a fresh full review, even without new commits (skips the delta shortcut) |
| `/review full level:beginner` | Combinations work — parameters can go together |

## How re-reviews behave

| Situation | Mode |
|---|---|
| You pushed new commits since the last review | **Delta review** — acknowledges what you fixed (see "Resolved since last review"), reports only what's still open or new |
| No new commits, but your comment has new parameters (`level:`, different focus, `full`) | **Full fresh review** with those parameters |
| No new commits, same parameters | **Brief no-change note** — compact table of open findings, no full re-review |

## Explanation levels

| Level | What you get |
|---|---|
| `beginner` | Full findings + **Learn corner**: what each bug class is, how it fails or gets exploited in the real world, why the fix works. Patient tone, jargon defined |
| `medium` (default) | What + why it matters + trade-off, compact |
| `advanced` | Flag, location, minimal fix hint. No trade-offs, no teaching |

Ways to set it (highest precedence first):

1. Per invocation: `/review level:beginner`
2. Caller workflow input: `with: explanation_level: beginner`
3. Repository variable: `REVIEWER_LEVEL` (Settings → Secrets and variables → Actions → Variables)

## Model selection

Ways to set it (highest precedence first):

1. Caller workflow input: `with: model: opencode-go/kimi-k3`
2. Repository variable: `REVIEWER_MODEL`
3. Default: `opencode-go/minimax-m3` (see the cost table in the README)

Any OpenCode model id works (`opencode-go/...` for the Go subscription catalog, `opencode/...` for Zen pay-as-you-go, or another provider with its own API-key secret, e.g. `ANTHROPIC_API_KEY`).

## Custom rubrics (per repo)

| Mechanism | Effect |
|---|---|
| `.github/reviewer.md` in the reviewed repo | **Overrides the default rubric entirely** — your severities, your checks, your tone |
| `rubrics/<stack>.md` in the reviewed repo | Per-stack overlay applied in addition to the base rubric (shipped defaults: `react.md`, `vue.md`, `python.md`) |
| `AGENTS.md` in the reviewed repo | Read automatically before reviewing — the reviewer judges against your conventions |
| Repo-local `.opencode/agent/reviewer.md` | Full vendoring: the central fetch is skipped and your local agent runs as-is |

## The review output

- **One GitHub Review** per invocation: summary body + inline comments on exact diff lines for P0/P1
- **Inline comments** carry `suggestion` blocks (batch-applicable "Apply suggestion" buttons) whenever the fix touches 1–3 lines
- **Summary sections**: Verdict · Scope · Resolved since last review (re-reviews) · P0 · P1 · P2 · P3 · Questions · Learn corner (beginner) · Notes & trade-offs (medium) · footer with rubrics and level applied
- **Verdicts are advisory**: `APPROVE` / `COMMENT` / `SUGGEST CHANGES`. The GitHub review event is always `COMMENT` — the bot never blocks a merge
- If the inline POST fails for any reason, the reviewer falls back to a plain summary comment — you never lose the review

## Typical flows

**Daily review loop**
```
/review                      → read findings
(apply suggestions in batch, or fix by hand, push)
/review                      → delta review confirms fixes, lists what's left
```

**Learning mode on a tricky PR**
```
/review level:beginner       → same findings + Learn corner explaining each bug class
```

**Second opinion on a sensitive area**
```
/review focus on the auth changes, level:advanced
```
