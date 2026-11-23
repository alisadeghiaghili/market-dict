# sonarqube-compliance — portable skill

A self-contained, agent-agnostic skill that forces SonarQube compliance on Python, R, and SQL (T-SQL / PL-SQL / Postgres) code, including **complete tests with 100% line + branch coverage on new/changed code**. Rule tables are a verified 2026-11-18 snapshot of `https://codeanalysis.ime.co.ir` (SonarQube 2026.4.0).

## Layout

```
sonarqube-compliance/
  SKILL.md                      ← entry point (the instructions)
  README.md                     ← this file
  references/
    python-rules.md             ← 498 rules
    tsql-rules.md               ← 82 rules
    plsql-rules.md              ← 189 rules
    postgres-rules.md           ← 12 rules
    r-rules.md                  ← R requirements (behavior spec — see note inside)
    testing-coverage.md         ← coverage + test-quality spec
    sonarqube-api.md            ← live-instance API guide
```

The skill is Markdown only — no code, no dependencies, no network requirement. `SKILL.md` is the contract; `references/` is loaded on demand.

## Installing per agent

### Claude Code / Claude
- Claude Code: copy the folder into the project: `cp -r sonarqube-compliance .claude/skills/` — it then loads automatically when the task matches (or say "use the sonarqube-compliance skill").
- Claude.ai / other Claude surfaces: attach `SKILL.md` (and the relevant `references/` files) to the conversation, or paste the `SKILL.md` content into custom instructions.

### OpenAI (Codex CLI / ChatGPT)
- Codex CLI: drop the folder into the repo (e.g. `docs/sonarqube-compliance/`) and add to `AGENTS.md`:
  > All Python, R, and SQL changes must follow `docs/sonarqube-compliance/SKILL.md` (load it before touching code).
- ChatGPT: attach `SKILL.md` (+ relevant references) per task, or put the core section in custom instructions.

### Antigravity (and AGENTS.md-compatible agents)
- Antigravity reads `AGENTS.md` project rules: paste the `SKILL.md` content into `AGENTS.md` (or reference it the same way as Codex above). It also works as a custom rule in the Rules panel — paste the `SKILL.md` body.

### Any other agent / LLM
- `SKILL.md` is plain imperative Markdown with YAML frontmatter you may keep or strip. Give the agent `SKILL.md` plus the reference files for the languages in scope, and the instructions are self-contained.

## Live verification (optional but recommended)

If the agent can reach the instance, set the token as an environment variable — **never in the repo**:

```
SONARQUBE_TOKEN=squ_...   # user token for codeanalysis.ime.co.ir
```

`references/sonarqube-api.md` has the verified endpoints (rule full text, open issues, measured coverage) and the 2026.x API gotchas. Without a token, the skill runs fully on the bundled snapshot.

## Updating the rule snapshot

When SonarQube or its plugins upgrade, re-pull and regenerate the tables:

```bash
# from this repo (needs node and the token in env)
node -e "/* see sonarqube-api.md for the exact endpoints */"
```

Concretely: `GET /api/rules/search?languages=<py|tsql|plsql|postgres>&ps=500&p=<n>` until `total` is reached, then rebuild the Markdown tables (key | name | severity | type | tags) and update the date in each file's header and in `SKILL.md`/`README.md`.
