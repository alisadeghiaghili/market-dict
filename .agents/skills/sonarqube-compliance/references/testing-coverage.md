# Tests & coverage — what SonarQube counts, and the bar this skill enforces

## Quality-gate targets

The instance's default gate is the standard "Sonar way" gate. **This skill enforces a stricter bar** — "fully tested" means:

| Metric | Typical instance gate | This skill's target |
|---|---|---|
| New bugs | 0 | 0 |
| New vulnerabilities | 0 | 0 |
| New security hotspots | 0 (all reviewed) | 0 |
| New code coverage | ≥ 80% | **100% line + branch on new/changed code** |
| New duplications | < 3% | 0% |
| New code smells | density ≤ 3% | 0 |

## Python

### What SonarQube counts as tests
- File patterns: `test_*.py`, `*_test.py` (override with `sonar.python.tests.included` / `sonar.python.tests.excluded`).
- Test code is excluded from production-code metrics **but is itself analyzed** against the test-quality rules below.

### Coverage
- Tool: `coverage.py` with **branch** enabled (`branch = true` in `[tool.coverage.run]` / `.coveragerc`).
- Run:
  ```bash
  pytest --cov=<package> --cov-branch --cov-report=term-missing --cov-report=xml:coverage.xml
  ```
- Scanner property: `sonar.python.coverage.reportPaths=coverage.xml` (or `sonar.coverage.reportPaths`).
- Delta coverage for the change:
  ```bash
  pip install diff-cover
  diff-cover coverage.xml --compare-branch=origin/main --fail-under=100
  ```
- **100% means**: every new/changed line executed, and **every branch outcome** taken by some test (`if/else`, both sides of `and/or`, `try/except`, loop-entry and loop-empty, default/raised).
- No exclusions (`--omit`, `coveragerc` omit) for new code. If a line is genuinely untestable (platform-specific path, defensive `except`), restructure the code — or get explicit user approval and state it in the report.

### Test-quality rules SonarQube applies to your test files
All 17 of these must be satisfied (full set, verified from the instance):

- `python:S5845` (CRITICAL, BUG) — never assert between incompatible types
- `python:S5899` — test methods must be discoverable (correct `test_` prefix, public)
- `python:S5905` (BLOCKER, BUG) — `assert (a, b)` asserts the tuple; assert each element
- `python:S5906` — use the most specific `unittest` assertion (`assertEqual`, `assertGreater`, …), not bare `assertTrue(x == y)`
- `python:S5914` — assertions must not pass or fail unconditionally
- `python:S5915` (CRITICAL, BUG) — no assertions at the end of a block expected to raise
- `python:S5918` — skip tests explicitly (`@pytest.mark.skip(reason=…)`), never comment them out
- `python:S2187` (BLOCKER) — a TestCase class must actually contain tests
- `python:S3415` — `assertEqual(actual, expected)` — correct argument order
- `python:S5778` — when testing a raised exception, exactly one method invocation inside the `pytest.raises` block
- `python:S5779` (CRITICAL, BUG) — never assert inside a `try` whose `except` catches `AssertionError`
- `python:S5863` — never pass the same argument to both sides of an assertion
- `python:S5958` — assert the **specific** exception type (and message where meaningful), not bare `Exception`
- `python:S5976` — group similar tests into one parameterized test (`@pytest.mark.parametrize`)
- `python:S8405` (BLOCKER) — FastAPI `TestClient`: use `content=` for bytes/text bodies
- `python:S8714` — use `pytest.raises` (dedicated exception assertion), not `try/except + fail()`
- `python:S1607` — `pytest.skip(...)` / `skipIf` must carry a reason

### Behavioral test requirements
- Deterministic: no real network (mock/fixture), no wall clock (`freezegun`/`monkeypatch`), no real filesystem outside `tmp_path`, fixed or mocked RNG seeds.
- One behavior per test; name = `test_<unit>_<scenario>_<expected>`.
- Cover: happy path, every branch, every error path, boundary values, empty inputs.
- No production logic guarded by `if TESTING:`; no monkeypatching that removes the very thing under test.

## R

See `r-rules.md` §4: testthat 3e under `tests/testthat/test-*.R`, no tautological tests, `skip()` only with a reason, `expect_error(regexp=)`, covr Cobertura XML to `sonar.coverage.reportPaths`, 100% line + branch on new/changed R code.

## SQL

- SonarQube computes **no coverage metric for SQL** — the bar is **zero issues** on the SQL files.
- Dynamic SQL must be parameterized (`sp_executesql` with `@params`, PL/SQL `EXECUTE IMMEDIATE … USING`, Postgres prepared statements / `format()` with `%L` only for literals you built) — this is what `tsql:S1523`, `plsql:S1523`, and the postgres `format()` rules enforce.
- Advisory (not measured by the scanner): for stored procedures/functions you change, exercise them against a disposable test schema with known fixtures and assert the result sets; keep those scripts under `tests/` so the next agent can rerun them.

## Definition of Done (run and show — never claim)

1. Lint mirror clean on touched files: `ruff check` (Python), `lintr::lint_dir()` (R).
2. Test suite green: `pytest -q`; `devtools::test()` for R.
3. Coverage measured: overall numbers **and 100% on changed lines** (`diff-cover` / covr delta).
4. Rule audit: the language's full rule table (see SKILL.md references) walked against the diff.
5. No secret/token in code, tests, config, or docs.
6. Final report contains the measured numbers and every user-approved deviation, with justification.
