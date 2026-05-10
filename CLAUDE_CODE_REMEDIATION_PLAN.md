# Claude Code Remediation Playbook

A senior-dev plan for getting every project onto a modern Claude Code setup: per-repo GitHub, configured harness, skills, subagents, hooks, and review automation.

Read top to bottom once. Then work the rollout in **Phase order** — don't skip ahead.

---

## TL;DR — the five things that matter most

If you only do five things, do these:

1. **Every project lives in its own GitHub repo, even private one-offs.** No more loose folders. Branch protection on `main`. (Phase 2)
2. **Every repo has a `CLAUDE.md` and `.claude/settings.json`.** This is the "harness" — it's how Claude knows your project's rules. (Phase 1)
3. **Two or three reusable Skills, not 20.** Start with `commit-and-push`, `pr-review`, and one project-type-specific one. (Phase 3)
4. **One or two Hooks for safety, not workflow.** Block writes to `.env`, run the linter on save. Don't over-automate. (Phase 5)
5. **`/security-review` before every PR merge.** It's free and it catches things. (Phase 6)

Everything else in this doc is optimization on top of those five.

---

## Mental model — how the pieces fit

Claude Code has roughly seven layers. Most people use one or two and wonder why it's not impressive.

| Layer | Lives in | What it's for |
|---|---|---|
| **CLAUDE.md** | Repo root (and `~/.claude/CLAUDE.md` for global) | Always-loaded instructions: stack, conventions, gotchas |
| **Settings** | `.claude/settings.json`, `~/.claude/settings.json` | Permissions, env vars, hooks, status line |
| **Skills** | `.claude/skills/<name>/SKILL.md` | Reusable instruction packets Claude loads on demand |
| **Subagents** | `.claude/agents/<name>.md` | Specialists Claude can delegate to (review, debug, plan) |
| **Slash commands** | `.claude/commands/<name>.md` | Custom `/foo` you type to trigger a prompt |
| **Hooks** | `.claude/settings.json` `"hooks"` block | Shell/HTTP commands that fire on events (pre-tool, post-edit, etc.) |
| **MCP servers** | `.mcp.json` (project) or settings (user) | External tools — GitHub, Slack, databases, etc. |

**Rule of thumb:**
- Stack and conventions → CLAUDE.md
- Repeatable workflows ("how I commit", "how I review a PR") → Skills
- Specialist roles ("the security reviewer", "the test writer") → Subagents
- Safety rails and chores ("don't write secrets", "format on save") → Hooks
- One-line shortcuts → Slash commands

---

## Phase 1 — Per-project foundation (the "harness")

Goal: every repo has the same basic shape, so jumping between them is frictionless.

### 1.1 Files every repo gets

```
<repo>/
├── CLAUDE.md                           ← project context (committed)
├── .claude/
│   ├── settings.json                   ← team settings (committed)
│   ├── settings.local.json             ← personal overrides (gitignored)
│   ├── skills/                         ← project-specific skills (committed)
│   ├── agents/                         ← project-specific subagents (committed)
│   └── commands/                       ← project-specific slash commands (committed)
├── .gitignore                          ← must exclude settings.local.json
└── .editorconfig                       ← consistent indentation across editors
```

### 1.2 `CLAUDE.md` template

Run `/init` in a fresh repo and Claude will draft this for you. Then trim it. Keep it under ~150 lines — it's loaded into every turn.

```markdown
# <Project Name>

## What this is
One sentence. What does this project do, who uses it.

## Stack
- Language: Python 3.12 / Node 20 / etc.
- Framework: FastAPI / Next.js / etc.
- Package manager: uv / pnpm / etc.
- Test runner: pytest / vitest / etc.

## Conventions
- Lint: `ruff check .` / `eslint .`
- Format: `ruff format .` / `prettier -w .`
- Test: `pytest` / `pnpm test`
- Type-check: `mypy .` / `tsc --noEmit`

## Run locally
```bash
<the actual commands>
```

## Don't
- Don't edit generated files in `dist/`, `build/`, `.next/`
- Don't commit secrets — `.env` is gitignored for a reason
- Don't bypass pre-commit hooks with `--no-verify`

## Architecture quick-ref
<2-5 bullet points about layout — where routes live, where the data layer is, etc.>
```

### 1.3 `.claude/settings.json` starter

```json
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./**/secrets.*)",
      "Edit(./.env)",
      "Edit(./.env.*)"
    ],
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(rg:*)",
      "Bash(pytest:*)",
      "Bash(npm test:*)",
      "Bash(pnpm test:*)"
    ]
  },
  "env": {
    "BASH_DEFAULT_TIMEOUT_MS": "120000"
  }
}
```

Tune the allow-list per project. Run `/fewer-permission-prompts` after a week of use — Claude will scan your transcripts and propose more entries.

### 1.4 `.gitignore` additions

Add these lines to every repo's `.gitignore`:

```
# Claude Code
.claude/settings.local.json
.claude/sessions/
.claude/backups/
```

`settings.local.json` is for **your machine only** (personal allowlists, env vars). Never commit it.

---

## Phase 2 — Each project on its own GitHub

Goal: stop having "loose folders" anywhere. Every project, even a 50-line script, gets its own repo.

### 2.1 Why per-repo (and not a monorepo)

For your situation (a portfolio of unrelated projects), per-repo wins because:
- Branch protection, secrets, and Actions are scoped per project
- Permissions and collaborators are scoped per project
- Issue trackers don't bleed together
- Each repo can have its own Claude Code config tuned to its stack

A monorepo only wins when projects share code or deploy together. If yours don't, don't.

### 2.2 The repo creation checklist

For each project, in order:

1. **Create the repo** (private by default)
   ```bash
   gh repo create <name> --private --source=. --remote=origin --push
   ```
2. **Add a meaningful README** — what it is, how to run it, one example
3. **Add a LICENSE** (MIT or Apache-2.0 unless you have a reason not to)
4. **Branch protection on `main`**
   - Require PR before merge
   - Require status checks (CI) to pass
   - Require branches up to date before merge
5. **Default branch = `main`**
6. **Set up CODEOWNERS** even if it's just you — `* @yourname`. Future-proofs collaboration.
7. **Add Dependabot or Renovate** (`.github/dependabot.yml`) — auto-PRs for security updates
8. **Add `.github/workflows/ci.yml`** — at minimum: install, lint, test, type-check
9. **Add `.github/PULL_REQUEST_TEMPLATE.md`** — Summary / Test plan / Risk
10. **Enable secret scanning** (free for private repos as of 2024) and **push protection**

### 2.3 The minimal CI workflow

`.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5  # or setup-node, etc.
        with:
          python-version: '3.12'
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: ruff format --check .
      - run: mypy .
      - run: pytest
```

Adapt to your stack. The point is: **lint + format + types + tests on every PR**, not just locally.

### 2.4 Once per repo: connect Claude Code

Inside each repo:
- Run `/init` to generate `CLAUDE.md`
- Trim it
- Commit `CLAUDE.md` and `.claude/settings.json`
- Add the `.gitignore` lines above

Now Claude Code is "aware" of that project the moment you open it.

---

## Phase 3 — Skills (your reusable playbooks)

A Skill is a markdown file with frontmatter that Claude loads when its trigger conditions match. Think of them as **muscle memory you teach Claude once**.

### 3.1 What to make Skills out of

Make a Skill when you find yourself explaining the **same workflow** to Claude more than twice. Examples:

- "How I commit" — your message style, what tests to run first, when to push
- "How I review a PR" — what to check, what to flag
- "How I set up a new feature branch"
- "How I write a migration"
- "How I bump a release"

**Don't** make Skills for one-offs. They cost context tokens.

### 3.2 Skill file structure

`.claude/skills/commit-and-push/SKILL.md`:

```markdown
---
name: commit-and-push
description: Stage relevant files, run tests, write a conventional-commit message, push to current branch. Use when the user says "commit", "ship it", or "push this".
---

## Steps

1. Run `git status` and `git diff` to see what changed.
2. If there are tests in this repo, run them first. Abort if any fail.
3. Stage only the files relevant to the task — never use `git add -A`.
4. Write a conventional-commit message (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`).
5. Commit, then push to the current branch (`git push -u origin HEAD`).
6. Report the commit SHA and any CI links.

## Don't
- Never use `--no-verify` to skip hooks. If a hook fails, fix the underlying issue.
- Never amend a pushed commit.
```

### 3.3 The starter Skill set every repo benefits from

| Skill | What it does |
|---|---|
| `commit-and-push` | The above |
| `pr-review` | Pull a PR, summarize, run tests against it, write review |
| `release-notes` | Diff `main` since last tag, draft CHANGELOG entry |
| `debug-failing-test` | Reproduce, isolate, fix, verify |

For project-specific Skills, examples:
- Web app: `add-api-endpoint`, `add-db-migration`
- Library: `cut-release`
- Data project: `add-pipeline-stage`

### 3.4 Built-in skills already there — use them

These ship with Claude Code, you don't need to write them:

- `/init` — generate CLAUDE.md
- `/review` — review a PR
- `/security-review` — security review of pending changes
- `/simplify` — find dead/duplicate code
- `/fewer-permission-prompts` — auto-generate allowlist
- `/team-onboarding` — generate ramp-up doc from your usage

---

## Phase 4 — Subagents (your specialists)

A subagent is a specialized Claude with its own system prompt, tool set, and optionally its own model. The main Claude can delegate to it via the `Task` tool.

### 4.1 When a subagent beats a skill

- Skill = "how to do this task" (instructions injected into main agent)
- Subagent = "a different role with its own context window" (separate conversation)

Use subagents when:
- The task pollutes the main context window (e.g., reading 30 files to find something)
- You want a fresh perspective (e.g., reviewer who hasn't seen your reasoning)
- The task is parallelizable (spawn 3 subagents to investigate 3 hypotheses)

### 4.2 Subagents worth defining

`.claude/agents/code-reviewer.md`:

```markdown
---
name: code-reviewer
description: Independent code reviewer. Use after a feature is done, before opening a PR.
tools: Read, Grep, Glob, Bash
---

You are a senior engineer doing an independent review.

Focus on:
1. Correctness — does the code do what was asked?
2. Edge cases — what inputs break it?
3. Tests — are they covering the actual behavior or just the happy path?
4. Security — any unsafe input handling, secrets, or auth gaps?

Report in three sections: **Must fix**, **Should fix**, **Nice to have**.
Don't restate what the code does. Don't praise.
```

Other useful ones:
- `test-writer` — given changed code, write tests
- `pr-investigator` — given a bug report, find the cause
- `dependency-auditor` — review `package.json` / `pyproject.toml` for risks

### 4.3 The Explore subagent (built-in)

For "find me X across this codebase" — use the built-in Explore agent. It's optimized for codebase search and uses Haiku to keep token costs low.

---

## Phase 5 — Hooks (your safety rails and chores)

Hooks fire on events: before a tool runs, after a file is edited, when the session starts, etc. They're shell or HTTP commands.

**Use hooks for safety and chores. Not for workflow.** If you find yourself writing complex hook logic, it should probably be a Skill or a subagent.

### 5.1 Hooks worth setting up

| Hook event | What it's for |
|---|---|
| `PreToolUse` | Block dangerous commands before they run |
| `PostToolUse` | Run formatter after Claude edits a file |
| `UserPromptSubmit` | Inject context into every prompt (e.g., current branch) |
| `SessionStart` | Set env vars, warm caches |
| `Stop` | Notify on long-running session completion |
| `PreCompact` | Save important context before auto-compaction |

### 5.2 Three starter hooks

In `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "if echo \"$CLAUDE_TOOL_INPUT\" | grep -qE '(rm -rf|--no-verify|force.push)'; then echo 'Blocked dangerous command' >&2; exit 2; fi"
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "if [ -f pyproject.toml ]; then ruff format \"$CLAUDE_FILE_PATH\" 2>/dev/null || true; fi"
        }]
      }
    ]
  }
}
```

The first blocks `rm -rf`, `--no-verify`, and force pushes. The second auto-formats Python files after Claude edits them. Adapt the second to your stack.

### 5.3 Don't over-hook

A hook that runs on every tool call adds latency to every tool call. If a hook isn't earning its cost, delete it. Run `/doctor` to see hook execution stats.

---

## Phase 6 — Code review pipeline

Goal: nothing reaches `main` without being reviewed. Half by humans, half by Claude.

### 6.1 The review flow per PR

1. **Open PR** with the template summary
2. **CI runs** (lint, format, types, tests)
3. **`/security-review`** — Claude scans the diff for security issues
4. **`/review`** — Claude does a general code review
5. **Optional: `/ultrareview`** — multi-agent deep review for high-risk PRs (paid feature, save it for the ones that matter)
6. **Human review** — you, a teammate, or both
7. **Merge** only when all four boxes are checked

### 6.2 Watch a PR with `subscribe_pr_activity`

After Claude opens a PR for you, ask: *"watch this PR and autofix CI failures or address review comments."* Claude subscribes to webhook events and wakes up when there's activity. You walk away.

### 6.3 The `--from-pr` shortcut

Resume the original session that created a PR:

```bash
claude --from-pr https://github.com/<you>/<repo>/pull/123
```

Useful when a PR review comes in days later and you forgot the context.

---

## Phase 7 — Safety & permissions

You said "don't do anything risky" — this section is the policy version of that.

### 7.1 The deny list every repo should have

In `.claude/settings.json` `permissions.deny`:

- `Read(./.env)`, `Read(./.env.*)`, `Edit(./.env*)` — secrets
- `Read(./**/secrets.*)`, `Read(./**/*.pem)`, `Read(./**/*.key)` — keys
- `Bash(rm -rf:*)` — destructive deletes
- `Bash(git push --force:*)` — force push
- `Bash(git reset --hard:*)` — destructive reset

### 7.2 Use Auto Mode for everyday work, not bypass mode

- **Default mode** — prompts on everything, slow but safe
- **Auto mode** — uses a classifier to allow safe things automatically; prompts on risky ones. **This is the sweet spot.**
- **`--dangerously-skip-permissions`** — full bypass. **Don't.** Reserve for sandboxed CI runs.

Toggle auto mode with `Shift+Tab` in any session, or set `permissions.defaultMode: "auto"` in settings.

### 7.3 Sandbox mode (Linux/Mac)

If your project mostly does file I/O and shell tasks, enable `sandbox.enabled: true` in settings. Bash commands run in a network/filesystem-restricted sandbox by default.

### 7.4 Secret hygiene

- Push protection on every GitHub repo (free tier includes it for public; you may need it explicitly enabled for private)
- Trufflehog or Gitleaks in CI as a backstop
- Pre-commit hook locally so secrets don't even reach the push stage

---

## What you're probably overlooking

A grab bag of things that aren't Claude Code features but are part of "having your projects in order":

| Thing | Why it matters |
|---|---|
| **Pre-commit framework** (lefthook / husky / pre-commit.com) | Lint + format + secret-scan before every commit, locally |
| **Conventional commits** | Auto-generate changelogs and version bumps |
| **`.editorconfig`** | Consistent indent/EOL across editors and contributors |
| **Dependabot or Renovate** | Auto-PRs for dependency updates |
| **CODEOWNERS** | Auto-assign reviewers, even if it's just you today |
| **PR template + Issue templates** | Enforces good summaries; future-you will thank you |
| **Status checks required on `main`** | Branch protection is meaningless without this |
| **`/usage`** | Watch your Claude Code rate limits before they bite |
| **`/context`** | See what's eating your context window — often it's a giant file or stale memory |
| **`/insights`** | Periodic "what is Claude actually doing in my sessions" report |
| **`/doctor`** | Health check; run after any config change |
| **MCP servers** | Connect Claude to GitHub, Slack, Linear, your DB, etc. — game changer for ops work |
| **Auto memory** | Claude now records and recalls facts across sessions; manage with `/memory` |
| **`--worktree`** flag | Run a session in an isolated git worktree — great for parallel experiments |
| **Status line customization** | Show project, branch, model, token usage in your terminal at a glance |
| **`/keybindings`** | Rebind shortcuts that conflict with your terminal/IDE |
| **Devcontainer** (`.devcontainer/devcontainer.json`) | Reproducible dev env; works with VS Code and GitHub Codespaces |

### MCP servers worth adding

Per project as needed, in `.mcp.json`:

- **GitHub MCP** — already wired in this environment, gives Claude PR/issue/repo access
- **Filesystem MCP** — extra directory access beyond the project root
- **Slack / Linear / Notion MCP** — if you use them, Claude can read/write
- **Postgres / SQLite MCP** — schema-aware DB queries

Don't add an MCP server you won't use. Each one adds tools that consume context tokens.

---

## Rollout order

Don't do this all at once. You'll burn out and abandon it.

### This week
1. Pick **one** project. Run `/init`, trim CLAUDE.md, commit it.
2. Add `.claude/settings.json` with the deny list from §7.1.
3. Add the gitignore lines from §1.4.
4. Push to GitHub if not there. Enable branch protection.

### This month
1. Repeat the above for **all** projects.
2. Write your first three Skills (§3.3).
3. Add the two starter hooks (§5.2) to your most-used repo.
4. Set up CI on every repo with the workflow from §2.3.
5. Enable Dependabot on every repo.

### Within three months
1. Build a `code-reviewer` subagent (§4.2).
2. Add `/security-review` to your PR checklist.
3. Try `subscribe_pr_activity` on a real PR.
4. Audit MCP servers — add the 1-2 that fit your workflow, skip the rest.
5. Run `/team-onboarding` to generate a ramp-up doc — even if the "team" is just future-you.

### Quarterly maintenance
- Run `/doctor` and address warnings
- Run `/fewer-permission-prompts` to refine allowlists
- Re-read each `CLAUDE.md` — kill stale instructions
- Review skills and subagents — delete unused ones
- Bump dependencies (Dependabot does most of this for you)

---

## What I'm explicitly **not** recommending

A few things from the changelog that look shiny but aren't worth the cognitive overhead for a solo developer:

- **Plugin marketplaces** — useful for teams; overkill for one person. Just put your skills in `~/.claude/skills/` for cross-project access.
- **Agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`)** — research-preview, expensive, narrow use case.
- **Voice mode** — fun, but doesn't make you faster.
- **Remote Control (`/remote-control`)** — skip unless you regularly need to drive Claude from your phone.
- **Custom themes / output styles** — pure cosmetic.
- **OpenTelemetry** — only worth setting up if you actually have a place to send the metrics.

You can always come back to these. Don't let them distract from the basics.

---

## How we'll work this

You're not doing this alone. The way I'd run this if I were your team lead:

1. **You pick the project** to start with.
2. **I (Claude) draft the changes** as a PR per project — `CLAUDE.md`, `.claude/settings.json`, `.gitignore` updates, CI workflow.
3. **You review and merge.**
4. **We move to the next.**

This way each project gets a clean, atomic PR you can audit before it lands. No big-bang rollout, no surprise changes.

When you're ready, point me at a project and say "start phase 1 here."
