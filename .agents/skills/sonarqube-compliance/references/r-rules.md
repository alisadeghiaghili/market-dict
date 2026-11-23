# R — SonarQube compliance requirements

> **Source note.** The SonarR plugin is **not installed** on `codeanalysis.ime.co.ir` (language key `r` returns 0 rules), and this machine has no internet access to SonarSource. This file therefore states the requirements as **enforced behavior**, reconstructed from SonarR's published rule categories (Reliability / Security / Maintainability, Clean Code attributes) and standard R lint practice (`lintr`, StatCheck). It deliberately lists **no rule keys** — inventing keys would be worse than none. Once SonarR is installed on the instance, sync the canonical list with `GET /api/rules/search?languages=r` and add the keys here.

## 1. Reliability (bug prevention)

| # | Requirement | What goes wrong otherwise |
|---|---|---|
| 1 | Use `seq_len(x)` / `seq_along(x)` — never `1:length(x)` | `1:0` returns `c(1, 0)`; loops misbehave on zero-length input |
| 2 | Test missingness with `is.na()`, `is.nan()`, `is.null()` — never `x == NA` | `== NA` yields `NA`, and `if (NA)` errors |
| 3 | Use only `TRUE` / `FALSE` — never `T` / `F` | `T` and `F` are reassignable user variables |
| 4 | Assign with `<-`; `=` is reserved for function arguments | mixing them silently changes meaning in nested calls |
| 5 | Compare floats with `all.equal()` / `expect_equal()` (with tolerance) — never `==` | `0.1 + 0.2 == 0.3` is `FALSE` |
| 6 | `if` conditions must be single logicals; never rely on implicit `if (c(TRUE, FALSE))` | R uses only the first element — silent logic bug |
| 7 | Guard empty input: `which.max`/`which.min` on empty/all-NA vectors, division by `length(x)`, `[1]` into an empty vector | returns `NA` or errors |
| 8 | Functions end in an explicit value (prefer `return(x)`); the last expression must be the documented return | side-effect-final statements return the wrong value invisibly |
| 9 | Never `source()` in production or package code; never `attach()` | namespace pollution, order-dependent behavior |
| 10 | Do not overwrite base function names (`mean`, `filter`, `sample`, …) | downstream code silently calls your function |
| 11 | `set.seed()` only in tests or documented reproducible experiments, with a comment | non-reproducible results |
| 12 | `options()` / `Sys.setenv()` changes must be scoped and restored (`on.exit`) | global state leaks across code |
| 13 | Temp files via `tempfile()`/`tempdir()`, cleaned in `on.exit`; no `setwd()` in production | predictable-path collisions, CWD drift |
| 14 | Avoid `sink()`; if unavoidable, pair with `on.exit(sink())` | output captured into a file forever |
| 15 | Never suppress warnings (`options(warn = -1)`, unjustified `suppressWarnings()`) | hides real signal problems |
| 16 | No `eval()` / `parse()` / `substitute()` on user-supplied strings; no `<<-` or `assign()` to globals | code injection, global mutation |
| 17 | `ifelse()` evaluates **both** branches — use `if`/`else` (or `dplyr::if_else()`) when one branch errors on the other's input | side effects run for every row |
| 18 | Be explicit about factors: `as.character()`, `as.factor()` with known levels | level reordering changes statistics |
| 19 | Date/time: use tz-aware objects (`POSIXct` with `tz=`, `lubridate`); never compare naive with aware | silent UTC-offset bugs |
| 20 | Avoid loops where vectorization works; use `vapply` with `FUN.VALUE`, not `sapply` type-guessing | performance and type surprises |
| 21 | `switch` needs a default; `stop()`/`stopifnot()` with informative messages at boundaries | cryptic failures |

## 2. Security

1. No `system()`, `shell()`, or `Rscript -e` with string-interpolated user input — build argument vectors and escape.
2. No remote code: `source("http://…")`, `url()` for code, `install.packages()` from unapproved repos; pin `repos`.
3. File paths from user input: `normalizePath()`, reject `..` traversal, write only to temp/sanitized locations.
4. No hard-coded connection strings, passwords, or API keys — use `Sys.getenv()`; env files stay out of the repository.
5. Cryptographic randomness: `runif()` is **not** crypto-grade — use `openssl::rand_bytes()` for tokens, IDs, salts.
6. Do not log or print data containing secrets or PII; no full `print()` of data frames in production paths.
7. Validate inputs at boundaries: types, ranges, and a documented `NA` policy per function.

## 3. Maintainability

1. Naming: `snake_case` for variables and functions; `UPPER_SNAKE_CASE` for constants; no single-letter names (except loop indices and plot axes); no Hungarian notation.
2. One concern per file; keep files ≲ 400 lines; function bodies ≲ 50 lines.
3. Cognitive complexity ≤ 15 per function; nesting ≤ 3 levels.
4. No unused variables, no unused function arguments (except interface-constrained `...`), no empty functions.
5. No commented-out code; `TODO`/`FIXME`/`HACK` comments are flagged — fix now or reference a tracked issue.
6. No duplicate literals beyond 3 occurrences — promote to a constant; no copy-pasted branches — extract a function.
7. No magic numbers — named constant with a comment.
8. Document every exported function with roxygen2: title, all args, return, value, example.
9. `library()` at file top only; in packages use `@import` / `::`; prefer `::` over `library()` inside functions.
10. Use `message()` for progress, `warning()`/`stop()` for conditions; no hand-rolled `cat()` newlines.
11. Indent 2 spaces, no tabs; line length ≤ 120; no trailing whitespace; file ends with a newline.
12. No global assignment from function bodies; structure as a package or a single-namespace module.
13. `invisible()` only where the invisibility is the point.

## 4. Tests & coverage (R)

- Framework: **testthat (3e)**. Files: `tests/testthat/test-<module>.R`.
- Every test: descriptive name (verb + object + case) and at least one meaningful `expect_*`; no tautologies (`expect_true(TRUE)`), no tests that only call code without asserting.
- `skip()` only with a reason; check raised errors with `expect_error(..., regexp = )` — the message, not just that something threw.
- Float comparisons: `expect_equal(..., tolerance = 1e-8)` or `all.equal()`.
- Deterministic: no network, no wall clock (mock time), no CWD dependence, no global state leaking between tests (`setup_*`/`teardown_*`).
- Coverage: `covr::package_coverage()` → export a **Cobertura XML** report (check your covr version's XML export; convert the standard report if needed) → point `sonar.coverage.reportPaths` at that XML.
- Target: **100% line + branch coverage on new/changed R code** (branches: `if`/`else` both outcomes, `&&`/`||` short-circuit cases, `switch` arms).

## 5. Verification before hand-off

Local mirror, run and show (never claim): `lintr::lint_dir()` clean on touched files, `devtools::test()` green, covr delta coverage on changed code at 100%.
