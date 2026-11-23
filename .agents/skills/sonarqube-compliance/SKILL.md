---
name: sonarqube-compliance
description: Enforce full SonarQube rule compliance (Python, R, SQL — T-SQL/PL-SQL/Postgres) plus 100% test coverage on new code. Use whenever writing, editing, reviewing, or generating Python, R, or SQL code that must pass the team's SonarQube quality gate, or when the user mentions SonarQube, sonar, quality gate, code smell, coverage, or open issues.
---

# SonarQube compliance

Hard requirement: any code touched under this skill must pass SonarQube with **zero new issues** (bugs, vulnerabilities, security hotspots, code smells) and **100% line + branch test coverage on new/changed code**. Scope: Python, R, and SQL (T-SQL, PL/SQL, Postgres).

## Workflow

1. Identify the language and dialect of every file in the change.
2. Load the matching reference (index below) and scan the rules that apply to what you are about to write. The full rule tables are the contract — a rule you did not consider is a rule you failed.
3. If the live instance is reachable (`SONARQUBE_TOKEN` set, see `references/sonarqube-api.md`) and you are fixing a specific rule, fetch its full text first: `GET /api/rules/show?key=<rule>`. If unreachable, the bundled references are a verified 2026-11-18 snapshot — use them.
4. Write the code, satisfying the top rules below **by construction** (no fix-up pass).
5. Write the tests: for every new/changed function — happy path, every branch outcome, every error path, boundary and empty inputs.
6. Run the verification loop: lint mirror (`ruff` for Python, `lintr` for R), full test suite, branch coverage, and delta coverage on the change (`diff-cover` / covr delta). If a line is untestable, restructure the code — do not exclude it.
7. Self-audit: walk the full rule table for the language against the diff; list the rules you verified in the final report.
8. Report: what changed, tests added, **measured** coverage numbers, rules audited, and any rule you believe is a false positive — with justification. Never silently ignore.

## Top Python rules (must be right by construction)

Injection and credentials:
- `python:S2077` / `pythonsecurity:S3649` — never build SQL by string formatting; parameterize every query.
- `pythonsecurity:S5334`, `pythonsecurity:S2076` — no `eval`/`exec`/`compile` on input; `subprocess` with argument lists, `shell=False`; validate command args (`pythonsecurity:S6350`).
- `pythonsecurity:S2083` — no path injection; `pythonsecurity:S6096` — zip-slip checks on archives.
- `python:S2068`, `python:S6418`, `python:S6437`, `pythonenterprise:S8435` — no hard-coded secrets/credentials, never in URL query params; env vars or a secret manager.
- `pythonsecurity:S8701`–`S8707` — agentic/AI workflow calls get the same injection treatment (command, SQL, SSRF, code, argument, connection-string, path).

Cryptography:
- `python:S4790` — no weak hashes (MD5/SHA-1 outside legacy); `python:S2053` + `python:S5344` — salted, slow password hashing (bcrypt/argon2/scrypt); `python:S2257` — no custom crypto; `python:S2245` — `secrets` module for anything security-relevant; `python:S5527`/`S4830` — verify TLS hostnames and certificates.

Bugs that break at runtime:
- `pythonbugs:S3518` — check denominators before dividing; `pythonbugs:S6464`/`S6466` — guard dict keys and sequence indexes.
- `python:S6725` — never compare to `numpy.nan` with `==`; use `np.isnan`/`pd.isna`.
- `pythonbugs:S6886`/`S6899` — never mix naive/aware datetimes, never compare `datetime` with `date`.
- `python:S2159` — no pointless equality checks; `python:S930` — call signatures must match.

Web frameworks:
- `python:S8392` — never bind web servers to all interfaces in dev code that ships; `python:S6779` — Flask secret key from env; `python:S8411` — FastAPI path params must appear in the signature; `python:S8400` — 204 responses have empty bodies.

## Top SQL rules

T-SQL:
- `tsql:S1523` — no `EXEC`/dynamic SQL with user-controlled data; `sp_executesql` + parameters.
- `tsql:S1590` — `DELETE`/`UPDATE` always need a `WHERE` clause.
- `tsql:S3641` — `NOT IN` with a nullable subquery silently returns no rows; use `NOT EXISTS`.

PL/SQL:
- `plsql:DeleteOrUpdateWithoutWhereCheck`, `plsql:PositionalAndNamedArgumentMixCheck`, `plsql:FunctionLastStatementReturnCheck`, `plsql:ForLoopUsageCheck` (no collection iteration in `FOR` loops), `plsql:S3830` (no `COMMIT` inside loops), `plsql:S1523`, `plsql:S2278` (no DES/3DES).

Postgres:
- `postgresdre:S8944`/`S8937` — `format()` placeholders: enough arguments, 1-based indexing; `postgresdre:S8788` — set-returning functions end with bare `RETURN`; `postgresdre:S8945` — no transaction control inside exception blocks.

General SQL:
- Explicit column lists in `INSERT`; no `SELECT *` in production queries; no functions on indexed columns in predicates (kills indexes); no `COMMIT` mid-loop; parameterize anything that carries data.

## R top requirements

Full checklist: `references/r-rules.md`. Non-negotiable core: `seq_len` over `1:length`; `is.na()` over `== NA`; `TRUE`/`FALSE` over `T`/`F`; `<-` for assignment; no `source()`/`attach()`/`eval()`/`system()` on user input; `all.equal()` for floats; roxygen2 docs on exported functions; `snake_case`; covr branch coverage 100% on new code via testthat 3e.

## Tests SonarQube counts — summary

- **Python**: `test_*.py` / `*_test.py` files; `coverage.py` with `branch = true`, XML report to `sonar.python.coverage.reportPaths`; the 17 test-quality rules (S5905, S5914, S2187, S5958, S8714, S1607, …) apply to the test code itself — full list in `references/testing-coverage.md`.
- **R**: testthat 3e, `tests/testthat/test-*.R`, covr Cobertura XML, no tautological tests.
- **SQL**: no coverage metric exists — zero issues is the bar; parameterized dynamic SQL is the security core.
- Target for all three: **100% line + branch on new/changed code** (strictly above the instance's default 80% gate).

## Definition of Done (all must be true, all must be shown)

- [ ] 0 new issues of any type on the diff (self-audited against the full rule tables)
- [ ] 100% line + branch coverage on new/changed code — **measured** (diff-cover / covr delta), not estimated
- [ ] Test suite green and deterministic (no network, wall clock, CWD, or global state dependence)
- [ ] Lint mirror (`ruff` / `lintr`) clean on touched files
- [ ] No secret or SonarQube token anywhere in code, tests, config, or docs
- [ ] Final report: changed files, tests added, measured coverage, rules audited, approved deviations

## Never

- Never hardcode the SonarQube token.
- Never suppress, disable, or exclude a rule to get green: no `# noqa: Sxxxx`, no `sonar.exclusions` for new files, no commented-out tests, no `skip()` without a reason — every deviation needs explicit user approval and appears in the report.
- Never claim a green gate or coverage number without running the check in this session.
- Never invent rule keys. If a rule is not in the references and the instance is unreachable, say so.

## References (load as needed)

| File | Content |
|---|---|
| `references/python-rules.md` | all 498 Python rules (2026-11-18 snapshot) |
| `references/tsql-rules.md` | all 82 T-SQL rules |
| `references/plsql-rules.md` | all 189 PL/SQL rules |
| `references/postgres-rules.md` | all 12 Postgres rules |
| `references/r-rules.md` | R requirements (SonarR not installed on the instance — behavior spec, no keys) |
| `references/testing-coverage.md` | quality-gate targets, coverage setup, 17 Python test rules, Definition of Done |
| `references/sonarqube-api.md` | live-instance REST API, verified endpoints and 2026.x gotchas |
| `README.md` | how to install this skill in Claude, Antigravity, Codex/OpenAI, and other agents |
