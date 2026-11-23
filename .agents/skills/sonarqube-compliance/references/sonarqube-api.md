# SonarQube live-instance API (verified 2026-11-18)

- Base URL: `https://codeanalysis.ime.co.ir` — SonarQube **2026.4.0**
- Auth: `Authorization: Bearer $SONARQUBE_TOKEN` (user token). Read the token from the environment; **never hardcode it** in code, tests, docs, or commits — that itself violates `python:S6418` / `python:S2068`.
- TLS: the host uses an internal CA. If the CA is not in the local trust store, disable certificate verification **only inside a throwaway query script** — never in product code.

## Language keys on this instance (verified)

| Language | Key | Rules |
|---|---|---|
| Python | `py` | 498 |
| T-SQL | `tsql` | 82 |
| PL/SQL | `plsql` | 189 |
| Postgres | `postgres` | 12 |
| R | `r` | **not installed (0)** — see `r-rules.md` |

## 2026.x API gotchas (verified empirically)

- Use `languages=` (plural). `language=` (singular) is **silently ignored** and returns all 8,353 rules.
- `activated=` is ignored — you cannot filter to the active set client-side. `GET /api/qualityprofiles/show?key=…&language=…` reports `activeRuleCount` (e.g. 454 for the Python *Sonar way* default profile).
- Removed in this build (404): `/api/plugins`, `/api/languages`, `/api/qualityprofiles/get_rules`.
- The HTML API browser (`/api`) returns 401 with a user token — it needs a web session; use REST only.
- `/api/projects/search` returned 403 for the verification token — take project keys from `sonar-project.properties` or the UI URL instead.

## Endpoints

| Purpose | Request |
|---|---|
| Instance up? | `GET /api/system/status` |
| Quality profiles | `GET /api/qualityprofiles/search` |
| Profile detail (active count) | `GET /api/qualityprofiles/show?key=<uuid>&language=py` |
| All rules for a language | `GET /api/rules/search?languages=py&ps=500&p=1` — paginate on `p` until `total` is reached |
| Full text of one rule | `GET /api/rules/show?key=python:S2077` → `descriptionSections[]` (introduction, root_cause, how_to_fix, examples), `impacts`, `params` |
| Open issues | `GET /api/issues/search?projects=<projectKey>&resolved=false&ps=100&facets=rules,severities,types` |
| Measures / coverage | `GET /api/measures/component?component=<projectKey>&metricKeys=coverage,covered_lines,total_lines,conditions,covered_conditions,new_coverage,duplications,bugs,vulnerabilities,security_hotspots,code_smells` |
| Analysis (CE) task | `GET /api/ce/task?id=<taskId>` |
| Source file | `GET /api/sources/show?fileKey=<componentKey>` |

## Examples

Node (bundled runtime; works):

```js
const res = await fetch('https://codeanalysis.ime.co.ir/api/rules/show?key=python:S2077', {
  headers: { Authorization: `Bearer ${process.env.SONARQUBE_TOKEN}` },
});
const { rule } = await res.json();
console.log(rule.descriptionSections.map((s) => s.content).join('\n'));
```

curl (internal cert — `-k` is fine for a throwaway check):

```bash
curl -k -H "Authorization: Bearer $SONARQUBE_TOKEN" \
  https://codeanalysis.ime.co.ir/api/system/status
```

## Live API vs bundled references

- The bundled references in this skill (`references/*-rules.md`) are a **2026-11-18 snapshot** — always sufficient for writing compliant code.
- Use the live API when: fixing a specific flagged issue (exact fix guidance + examples from `descriptionSections`), checking a project's open issues or measured coverage, or after a SonarQube/plugin upgrade (re-snapshot the references, then delete the old file's date and note the new one).
