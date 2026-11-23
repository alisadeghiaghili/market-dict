# T-SQL rules — full SonarQube set

Source: codeanalysis.ime.co.ir (SonarQube 2026.4.0), pulled 2026-11-18 via /api/rules/search (language key `tsql`).
Total: **82** rules. By type: CODE_SMELL=62, VULNERABILITY=4, BUG=16.
By severity: BLOCKER=3, CRITICAL=19, INFO=1, MAJOR=44, MINOR=15.

Every rule below is a hard requirement for new code in this skill. Before writing code that a rule touches, read the rule's full text on the live instance (`GET /api/rules/show?key=<rule>` — see `sonarqube-api.md`); if the instance is unreachable, the rule name and severity here are the guidance.

| Key | Rule | Severity | Type | Tags |
|---|---|---|---|---|
| tsql:S103 | Lines should not be too long | MAJOR | CODE_SMELL | convention |
| tsql:S104 | Files should not have too many lines of code | MAJOR | CODE_SMELL | brain-overload |
| tsql:S105 | Tabulation characters should not be used | MINOR | CODE_SMELL | convention |
| tsql:S107 | Functions and procedures should not have too many parameters | MAJOR | CODE_SMELL | brain-overload |
| tsql:S117 | Local variable and parameter names should comply with a naming convention | MINOR | CODE_SMELL | convention |
| tsql:S121 | Control structures should use BEGIN...END blocks | CRITICAL | CODE_SMELL | pitfall |
| tsql:S122 | Statements should be on separate lines | MAJOR | CODE_SMELL | convention |
| tsql:S125 | Sections of code should not be commented out | MAJOR | CODE_SMELL | unused |
| tsql:S126 | "IF ... ELSEIF" constructs should end with "ELSE" clauses | CRITICAL | CODE_SMELL |  |
| tsql:S131 | "CASE" expressions should end with "ELSE" clauses | CRITICAL | CODE_SMELL | cwe |
| tsql:S134 | Control flow statements "IF", "WHILE" and "TRY" should not be nested too deeply | CRITICAL | CODE_SMELL | brain-overload |
| tsql:S138 | Functions and stored procedure should not have too many lines of code | MAJOR | CODE_SMELL | brain-overload |
| tsql:S907 | "GOTO" statements should not be used | MAJOR | CODE_SMELL | brain-overload |
| tsql:S1065 | Unused labels should be removed | MAJOR | CODE_SMELL | unused |
| tsql:S1066 | Mergeable "if" statements should be combined | MAJOR | CODE_SMELL | clumsy |
| tsql:S1067 | Expressions should not be too complex | CRITICAL | CODE_SMELL | brain-overload |
| tsql:S1110 | Unnecessary parentheses should be removed | MINOR | CODE_SMELL | readability, redundant |
| tsql:S1116 | Empty statements should be removed | MINOR | CODE_SMELL | unused |
| tsql:S1134 | Track uses of "FIXME" tags | MAJOR | CODE_SMELL | cwe |
| tsql:S1135 | Track uses of "TODO" tags | INFO | CODE_SMELL | cwe |
| tsql:S1151 | "WHEN" clauses should not have too many lines of code | MAJOR | CODE_SMELL | brain-overload |
| tsql:S1172 | Unused procedure and function parameters should be removed | MAJOR | CODE_SMELL | unused |
| tsql:S1192 | String literals should not be duplicated | CRITICAL | CODE_SMELL | design |
| tsql:S1313 | IP addresses should not be hardcoded | MINOR | CODE_SMELL | former-hotspot |
| tsql:S1451 | Track lack of copyright and license headers | BLOCKER | CODE_SMELL | convention |
| tsql:S1479 | "CASE" expressions should not have too many "WHEN" clauses | MAJOR | CODE_SMELL | brain-overload |
| tsql:S1481 | Unused local variables should be removed | MINOR | CODE_SMELL | unused |
| tsql:S1499 | Columns to be read with a "SELECT" statement should be clearly defined | MAJOR | CODE_SMELL | performance, sql |
| tsql:S1523 | Dynamic code execution should not use user-controlled data | CRITICAL | VULNERABILITY | cwe, former-hotspot |
| tsql:S1542 | Function and procedure names should comply with a naming convention | MAJOR | CODE_SMELL | convention |
| tsql:S1590 | "DELETE" and "UPDATE" statements should contain "WHERE" clauses | BLOCKER | BUG | sql |
| tsql:S1614 | A primary key should be specified during table creation | BLOCKER | CODE_SMELL | suspicious |
| tsql:S1631 | Queries should not join too many tables | MAJOR | CODE_SMELL | performance, brain-overload, sql |
| tsql:S1656 | Variables should not be self-assigned | MAJOR | BUG |  |
| tsql:S1659 | Multiple variables should not be declared on the same line | MINOR | CODE_SMELL | convention |
| tsql:S1735 | Column names should be used in an "ORDER BY" clause | MAJOR | CODE_SMELL | sql |
| tsql:S1739 | "LIKE" clauses should not start with wildcard characters | MAJOR | CODE_SMELL | performance, sql |
| tsql:S1742 | Non-standard comparison operators should not be used | MINOR | CODE_SMELL | lock-in, sql |
| tsql:S1745 | "INSERT" statements should explicitly list the columns to be set | CRITICAL | CODE_SMELL | sql |
| tsql:S1751 | Loops with at most one iteration should be refactored | MAJOR | BUG | bad-practice, confusing |
| tsql:S1763 | All code should be reachable | MAJOR | BUG | cwe, unused |
| tsql:S1764 | Identical expressions should not be used on both sides of a binary operator | MAJOR | BUG | suspicious |
| tsql:S1862 | Related "IF"/"ELSE IF" statements and "WHEN" clauses in a "CASE" should not have the same condition | MAJOR | BUG | unused, pitfall |
| tsql:S1871 | Two branches in a conditional structure should not have exactly the same implementation | MAJOR | CODE_SMELL | design, suspicious |
| tsql:S1940 | Boolean checks should not be inverted | MINOR | CODE_SMELL | pitfall |
| tsql:S2068 | Credentials should not be hard-coded | MAJOR | VULNERABILITY | cwe, former-hotspot |
| tsql:S2070 | SHA-1 and Message-Digest hash algorithms should not be used in secure contexts | CRITICAL | VULNERABILITY |  |
| tsql:S2260 | Track parsing failures | MAJOR | CODE_SMELL | suspicious |
| tsql:S2527 | "NULL" should not be compared directly | MAJOR | BUG | sql |
| tsql:S2681 | Multiline blocks should be enclosed in BEGIN...END blocks | MAJOR | CODE_SMELL | cwe |
| tsql:S2737 | "CATCH" clauses should do more than rethrow | MINOR | CODE_SMELL | error-handling, unused, finding, clumsy |
| tsql:S2761 | Unary prefix operators should not be repeated | MAJOR | BUG |  |
| tsql:S3358 | Ternary operators should not be nested | MAJOR | CODE_SMELL | confusing |
| tsql:S3626 | Jump statements should not be redundant | MINOR | CODE_SMELL | redundant, clumsy |
| tsql:S3633 | "WHERE" clause conditions should not be contradictory | MAJOR | BUG | sql |
| tsql:S3641 | Nullable subqueries should not be used in "NOT IN" conditions | CRITICAL | BUG | sql |
| tsql:S3643 | "LIKE" clauses should not be used without wildcards | MINOR | CODE_SMELL | sql |
| tsql:S3650 | "WHERE" clauses should not contain redundant conditions | MAJOR | BUG | sql |
| tsql:S3923 | All branches in a conditional structure should not have exactly the same implementation | MAJOR | BUG |  |
| tsql:S3972 | Conditionals should start on new lines | CRITICAL | CODE_SMELL | suspicious |
| tsql:S3973 | Conditionally executed code should be denoted by either indentation or BEGIN...END block | CRITICAL | CODE_SMELL | confusing, suspicious |
| tsql:S4054 | Queries that use "TOP" should have an "ORDER BY" | MAJOR | BUG | sql |
| tsql:S4075 | Deprecated features should not be used | MAJOR | CODE_SMELL | obsolete |
| tsql:S4078 | Size should be specified for "varchar" variables and parameters | CRITICAL | CODE_SMELL | suspicious |
| tsql:S4094 | "CASE" input expressions should be invariant | CRITICAL | BUG | unpredictable |
| tsql:S4102 | "CHECK" or "NOCHECK" should be specified explicitly when constraints are activated | MAJOR | CODE_SMELL | pitfall |
| tsql:S4103 | The number of variables in a FETCH statement should match the number of columns in the cursor | CRITICAL | BUG |  |
| tsql:S4104 | "COALESCE", "IIF", and "CASE" input expressions should not contain subqueries | MAJOR | CODE_SMELL | unpredictable |
| tsql:S4108 | "@@IDENTITY" should not be used | MAJOR | CODE_SMELL | unpredictable, suspicious |
| tsql:S4109 | Triggers should not "PRINT", "SELECT", or "FETCH" | MINOR | CODE_SMELL | unused |
| tsql:S4142 | Duplicate values should not be passed as arguments | MAJOR | CODE_SMELL |  |
| tsql:S4149 | Column references should not have more than two-parts | MINOR | CODE_SMELL | obsolete |
| tsql:S4154 | "ANSI_NULLS", "ANSI_PADDING" and "CONCAT_NULL_YIELDS_NULL" should not be configured | MAJOR | CODE_SMELL | obsolete |
| tsql:S4155 | Deprecated system tables and views should not be used | MAJOR | CODE_SMELL | obsolete |
| tsql:S4196 | Output parameters should be assigned | MAJOR | BUG | pitfall |
| tsql:S4413 | Reserved keywords should not be used as identifiers or object names | MINOR | CODE_SMELL |  |
| tsql:S4790 | Weak hashing algorithms should not be used | CRITICAL | VULNERABILITY | cwe, former-hotspot |
| tsql:S4801 | "SELECT" statements used as argument of "EXISTS" statements should be selective | CRITICAL | CODE_SMELL |  |
| tsql:S4819 | "NOCOUNT" should be activated on "PROCEDURE" and "TRIGGER" definitions | CRITICAL | CODE_SMELL | performance |
| tsql:S4820 | Track lack of SQL Server session configuration | MAJOR | CODE_SMELL |  |
| tsql:S6498 | "ANSI_WARNINGS" and "ARITHABORT" options should not be set to OFF | CRITICAL | CODE_SMELL | error-handling, performance, unpredictable |
| tsql:NoSonar | Track uses of "NOSONAR" comments | MAJOR | CODE_SMELL | bad-practice |
