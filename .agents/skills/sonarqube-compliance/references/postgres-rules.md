# Postgres rules — full SonarQube set

Source: codeanalysis.ime.co.ir (SonarQube 2026.4.0), pulled 2026-11-18 via /api/rules/search (language key `postgres`).
Total: **12** rules. By type: CODE_SMELL=5, BUG=7.
By severity: CRITICAL=7, MAJOR=3, MINOR=2.

Every rule below is a hard requirement for new code in this skill. Before writing code that a rule touches, read the rule's full text on the live instance (`GET /api/rules/show?key=<rule>` — see `sonarqube-api.md`); if the instance is unreachable, the rule name and severity here are the guidance.

| Key | Rule | Severity | Type | Tags |
|---|---|---|---|---|
| postgresdre:S2260 | Postgres source files should not have syntax errors | MAJOR | CODE_SMELL | suspicious |
| postgresdre:S8788 | Set-Returning Functions should terminate with bare "RETURN" after "RETURN NEXT" or "RETURN QUERY" | CRITICAL | BUG | plpgsql, pitfall |
| postgresdre:S8933 | Composite primary keys should not contain more than four columns | MAJOR | CODE_SMELL |  |
| postgresdre:S8934 | Schemas should not grant CREATE privilege to PUBLIC | MINOR | CODE_SMELL |  |
| postgresdre:S8935 | Format strings should have properly terminated conversion specifiers | CRITICAL | BUG | pitfall |
| postgresdre:S8937 | Format placeholders in "format()" should use 1-based indexing | CRITICAL | BUG | pitfall |
| postgresdre:S8938 | Indirect-width format specifiers should include a dollar sign after the width position | CRITICAL | BUG | plpgsql, pitfall, sql |
| postgresdre:S8939 | PL/pgSQL protected automatic variables should not be modified | CRITICAL | BUG | plpgsql, pitfall |
| postgresdre:S8942 | Identifiers should not use reserved SQL keywords | MINOR | CODE_SMELL | plpgsql |
| postgresdre:S8943 | Unused arguments in PostgreSQL "format()" calls should be removed | MAJOR | CODE_SMELL | unused |
| postgresdre:S8944 | PostgreSQL "format()" calls should provide enough arguments for all placeholders | CRITICAL | BUG |  |
| postgresdre:S8945 | Transaction control statements should not be used inside exception handling blocks | CRITICAL | BUG | plpgsql, pitfall |
