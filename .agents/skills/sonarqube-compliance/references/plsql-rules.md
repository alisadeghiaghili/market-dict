# PL/SQL rules — full SonarQube set

Source: codeanalysis.ime.co.ir (SonarQube 2026.4.0), pulled 2026-11-18 via /api/rules/search (language key `plsql`).
Total: **189** rules. By type: CODE_SMELL=138, BUG=45, VULNERABILITY=6.
By severity: BLOCKER=26, CRITICAL=34, INFO=1, MAJOR=90, MINOR=38.

Every rule below is a hard requirement for new code in this skill. Before writing code that a rule touches, read the rule's full text on the live instance (`GET /api/rules/show?key=<rule>` — see `sonarqube-api.md`); if the instance is unreachable, the rule name and severity here are the guidance.

| Key | Rule | Severity | Type | Tags |
|---|---|---|---|---|
| plsql:S104 | Files should not have too many lines of code | MAJOR | CODE_SMELL | brain-overload |
| plsql:S125 | Sections of code should not be commented out | MAJOR | CODE_SMELL | unused |
| plsql:S126 | "IF ... ELSEIF" constructs should end with "ELSE" clauses | CRITICAL | CODE_SMELL |  |
| plsql:S131 | "CASE" statements should end with "ELSE" clauses | CRITICAL | CODE_SMELL | cwe |
| plsql:S139 | Comments should not be located at the end of lines of code | MINOR | CODE_SMELL | convention |
| plsql:S1066 | Mergeable "if" statements should be combined | MAJOR | CODE_SMELL | clumsy |
| plsql:S1110 | Unnecessary parentheses should be removed | MINOR | CODE_SMELL | readability, redundant |
| plsql:S1117 | Variables should not be shadowed | MAJOR | CODE_SMELL | suspicious, pitfall |
| plsql:S1126 | Return of boolean expressions should not be wrapped into an "if-then-else" statement | MINOR | CODE_SMELL | clumsy |
| plsql:S1131 | Lines should not end with trailing whitespaces | MINOR | CODE_SMELL | convention |
| plsql:S1134 | Track uses of "FIXME" tags | MAJOR | CODE_SMELL | cwe |
| plsql:S1135 | Track uses of "TODO" tags | INFO | CODE_SMELL | cwe |
| plsql:S1138 | SQL EXISTS subqueries should not be used | MAJOR | CODE_SMELL | performance, sql |
| plsql:S1145 | "IF" statement conditions should not evaluate unconditionally to "TRUE" or to "FALSE" | MAJOR | BUG | cwe |
| plsql:S1151 | "WHEN" clauses should not have too many lines | MAJOR | CODE_SMELL | brain-overload |
| plsql:S1172 | Unused procedure and function parameters should be removed | MAJOR | CODE_SMELL | unused |
| plsql:S1192 | String literals should not be duplicated | CRITICAL | CODE_SMELL | design |
| plsql:S1451 | Track lack of copyright and license headers | BLOCKER | CODE_SMELL | convention |
| plsql:S1479 | "CASE" structures should not have too many "WHEN" clauses | MAJOR | CODE_SMELL | brain-overload |
| plsql:S1481 | Unused local variables should be removed | MINOR | CODE_SMELL | unused |
| plsql:S1523 | Dynamic code execution should not use user-controlled data | CRITICAL | VULNERABILITY | cwe, former-hotspot |
| plsql:S1573 | Explicitly opened cursors should be closed | MINOR | BUG | cwe, sql |
| plsql:S1614 | A primary key should be specified during table creation | BLOCKER | CODE_SMELL | suspicious |
| plsql:S1615 | Constraint names should comply with a naming convention | MINOR | CODE_SMELL | convention |
| plsql:S1656 | Variables and columns should not be self-assigned | MAJOR | BUG |  |
| plsql:S1703 | "%TYPE" and "%ROWTYPE" should not be used in package specification | CRITICAL | CODE_SMELL |  |
| plsql:S1739 | "LIKE" clauses should not start with wildcard characters | MAJOR | CODE_SMELL | performance, sql |
| plsql:S1745 | "INSERT" statements should explicitly list the columns to be set | CRITICAL | CODE_SMELL | sql |
| plsql:S1751 | Loops with at most one iteration should be refactored | MAJOR | BUG | bad-practice, confusing |
| plsql:S1764 | Identical expressions should not be used on both sides of a binary operator | MAJOR | BUG | suspicious |
| plsql:S1854 | Unused assignments should be removed | MAJOR | CODE_SMELL | cwe, unused |
| plsql:S1862 | Related "IF/ELSIF" statements and "WHEN" clauses in a "CASE" should not have the same condition | MAJOR | BUG | unused, pitfall |
| plsql:S1871 | Two branches in a conditional structure should not have exactly the same implementation | MAJOR | CODE_SMELL | design, suspicious |
| plsql:S1940 | Boolean checks should not be inverted | MINOR | CODE_SMELL | pitfall |
| plsql:S2070 | SHA-1 and Message-Digest hash algorithms should not be used in secure contexts | CRITICAL | VULNERABILITY |  |
| plsql:S2278 | Neither DES (Data Encryption Standard) nor DESede (3DES) should be used | BLOCKER | VULNERABILITY | cwe |
| plsql:S2737 | "EXCEPTION WHEN ... THEN" clauses should do more than "RAISE" | MINOR | CODE_SMELL | error-handling, unused, finding, clumsy |
| plsql:S2761 | Unary prefix operators should not be repeated | MAJOR | BUG |  |
| plsql:S3618 | Inserts should include values for non-null columns | BLOCKER | BUG | sql |
| plsql:S3626 | Jump statements should not be redundant | MINOR | CODE_SMELL | redundant, clumsy |
| plsql:S3633 | "WHERE" clause conditions should not be contradictory | MAJOR | BUG | sql |
| plsql:S3641 | Nullable subqueries should not be used in "NOT IN" conditions | CRITICAL | BUG | sql |
| plsql:S3643 | "LIKE" clauses should not be used without wildcards | CRITICAL | CODE_SMELL | sql |
| plsql:S3651 | Individual "WHERE" clause conditions should not be unconditionally true or false | CRITICAL | BUG | sql |
| plsql:S3830 | "COMMIT" should not be used inside a loop | CRITICAL | BUG |  |
| plsql:S3921 | Strings should only be moved to variables or columns which are large enough to hold them | MAJOR | BUG | cwe |
| plsql:S3923 | All branches in a conditional structure should not have exactly the same implementation | MAJOR | BUG |  |
| plsql:S4062 | "ROWNUM" should not be used at the same query level as "ORDER BY" | MAJOR | BUG | sql |
| plsql:S4081 | "PLS_INTEGER" types should be used | MINOR | CODE_SMELL | performance |
| plsql:S4196 | Output parameters should be assigned | MAJOR | BUG | pitfall |
| plsql:S4421 | Features deprecated in Oracle 12 should not be used | MAJOR | CODE_SMELL | obsolete |
| plsql:S4575 | "TO_DATE" and "TO_TIMESTAMP" should be used with a datetime format model | MAJOR | CODE_SMELL |  |
| plsql:S4576 | "FORMS_DDL('COMMIT')" and "FORMS_DDL('ROLLBACK')" should not be used | CRITICAL | BUG |  |
| plsql:S4577 | "SYNCHRONIZE" should not be used | BLOCKER | BUG | performance |
| plsql:S4584 | "CREATE_TIMER" should not be used | MAJOR | CODE_SMELL | performance |
| plsql:S4790 | Weak hashing algorithms should not be used | CRITICAL | VULNERABILITY | cwe, former-hotspot |
| plsql:S4801 | "SELECT" statements used as argument of "EXISTS" statements should be selective | CRITICAL | CODE_SMELL |  |
| plsql:S5047 | "TO_NUMBER" should be used with a format model | MAJOR | CODE_SMELL |  |
| plsql:S5141 | SQL "JOIN" conditions should involve all joined tables | CRITICAL | CODE_SMELL |  |
| plsql:S5245 | Identifiers should be written in lower case | MINOR | CODE_SMELL | convention |
| plsql:S5547 | Cipher algorithms should be robust | CRITICAL | VULNERABILITY | cwe, privacy |
| plsql:S6467 | Features deprecated in Oracle 18 should not be used | MAJOR | CODE_SMELL | obsolete |
| plsql:AnchoredTypeConstrainCheck | Anchored types should not be constrained | BLOCKER | BUG |  |
| plsql:AvoidFetchBulkCollectIntoWithoutLimitCheck | "FETCH ... BULK COLLECT INTO" should not be used without a "LIMIT" clause | BLOCKER | BUG |  |
| plsql:AvoidGroupByClauseCheck | "GROUP BY" should not be used in SQL "SELECT" statements | MAJOR | CODE_SMELL | performance, brain-overload, sql |
| plsql:BackwardsGoto | GOTO should not be used to jump backwards | BLOCKER | CODE_SMELL | pitfall |
| plsql:BadRaiseApplicationErrorUsageCheck | "RAISE_APPLICATION_ERROR" should only be used with error codes from -20,000 to -20,999 | BLOCKER | BUG | error-handling |
| plsql:BlockMissingSemicolonCheck | Block labels should appear on the same lines as "END" | CRITICAL | CODE_SMELL | convention |
| plsql:BlockUnlabeledEndCheck | "END" statements of labeled blocks should be labeled | MAJOR | CODE_SMELL | convention |
| plsql:BooleanLiteralComparisonCheck | Boolean literals should not be redundant | MINOR | CODE_SMELL | clumsy |
| plsql:CharVarchar | "VARCHAR2" and "NVARCHAR2" should be used | MAJOR | BUG |  |
| plsql:ColumnsShouldBeAliasedCheck | Columns should be aliased | MAJOR | CODE_SMELL | design, sql |
| plsql:CommentRegularExpressionCheckPlSql | Track comments matching a regular expression | MAJOR | CODE_SMELL |  |
| plsql:ComplexIfShouldBeReplacedByCase | CASE should be used for sequences of simple tests | MINOR | CODE_SMELL | clumsy |
| plsql:CompoundTriggerDefinesSingleTrigger | Compound triggers should define at least two triggers | MAJOR | CODE_SMELL | clumsy |
| plsql:ConstantDeclarationWithoutInitializationCheck | Constant declarations should contain initialization assignments | BLOCKER | BUG |  |
| plsql:CreateOrReplaceCheck | "CREATE OR REPLACE" should be used instead of "CREATE" | CRITICAL | CODE_SMELL | bad-practice |
| plsql:CrossJoinUsageCheck | "CROSS JOIN" queries should not be used | MAJOR | CODE_SMELL | suspicious |
| plsql:CustomExceptionInitCheck | "EXCEPTION_INIT -20,NNN" calls should be centralized | CRITICAL | CODE_SMELL | design |
| plsql:DbmsOutputPutLineCallCheck | "DBMS_OUTPUT.PUT_LINE" should not be used | CRITICAL | CODE_SMELL | bad-practice |
| plsql:DeadCodeCheck | All code should be reachable | MAJOR | BUG | cwe, unused |
| plsql:DecodeFunctionUsageCheck | "CASE" should be used rather than "DECODE" | MAJOR | CODE_SMELL | obsolete |
| plsql:DeleteOrUpdateWithoutWhereCheck | "DELETE" and "UPDATE" statements should contain "WHERE" clauses | BLOCKER | BUG | sql |
| plsql:ExecuteImmediateTrapExceptionsCheck | Blocks containing "EXECUTE IMMEDIATE" should trap all exceptions | CRITICAL | CODE_SMELL | error-handling |
| plsql:ExitInLoop | "EXIT" should not be used in loops | MINOR | CODE_SMELL | bad-practice |
| plsql:FloatWithScaleUsageCheck | Scale should not be specified for float types | BLOCKER | BUG |  |
| plsql:ForLoopUsageCheck | Collections should not be iterated in "FOR" loops | CRITICAL | BUG |  |
| plsql:ForallStatementShouldUseSaveExceptionsClause | "FORALL" statements should use the "SAVE EXCEPTIONS" clause | BLOCKER | BUG |  |
| plsql:FormatErrorStackAndBacktraceUsedAlongside | "DBMS_UTILITY.FORMAT_ERROR_STACK" and "FORMAT_ERROR_BACKTRACE" should be used together | MINOR | CODE_SMELL | error-reporting |
| plsql:FullOuterJoinCheck | "FULL OUTER JOINS" should be used with caution | MAJOR | CODE_SMELL | pitfall, sql |
| plsql:FunctionLastStatementReturnCheck | Functions should end with "RETURN" statements | CRITICAL | BUG | pitfall |
| plsql:FunctionOutParametersCheck | "FUNCTIONS" should not have "OUT" parameters | MAJOR | CODE_SMELL | suspicious, pitfall |
| plsql:FunctionResultCacheCheck | "RESULT_CACHE" should not be used | MAJOR | CODE_SMELL | performance |
| plsql:GotoInLoopCheck | "GOTO" should not be used within loops | MAJOR | CODE_SMELL | pitfall |
| plsql:ImproperConstraintUsageCheck | Improper constraint forms should not be used | BLOCKER | BUG |  |
| plsql:InItemsCountCheck | Large item lists should not be used with "IN" clauses | MAJOR | CODE_SMELL | pitfall, sql |
| plsql:InitializeWithNullCheck | Variables should not be initialized with "NULL" | MINOR | CODE_SMELL | clumsy |
| plsql:InvalidConstrainCheck | Constraints should not be applied to types that cannot be constrained | BLOCKER | BUG |  |
| plsql:JoinConditionNumberCheck | SQL statements should not join too many tables | MAJOR | CODE_SMELL | performance, brain-overload, sql |
| plsql:LabelStartEndMatchBlockCheck | Block start and end labels should match | BLOCKER | CODE_SMELL | confusing |
| plsql:LabelStartEndMatchLoopCheck | Loop start and end labels should match | BLOCKER | CODE_SMELL | confusing |
| plsql:LabelSubBlock | Nested blocks should be labeled | MAJOR | CODE_SMELL | convention |
| plsql:LabeledNestedLoopsCheck | Nested loops should be labeled | MAJOR | CODE_SMELL | convention, confusing |
| plsql:LineLength | Lines should not be too long | MAJOR | CODE_SMELL | convention |
| plsql:LiteralsNonPrintableCharactersCheck | Whitespace and control characters in string literals should be explicit | CRITICAL | CODE_SMELL | pitfall |
| plsql:LongCheck | Deprecated LONG and LONG RAW datatypes should no longer be used | MAJOR | CODE_SMELL | obsolete |
| plsql:LoopAvoidSimpleLoopCheck | "LOOP ... END LOOP;" constructs should be avoided | CRITICAL | CODE_SMELL | pitfall |
| plsql:LoopHardcodedBoundsCheck | "FOR" loop end conditions should not be hard-coded | MAJOR | CODE_SMELL | brain-overload |
| plsql:LoopMissingSemicolonCheck | "END LOOP" should be followed by a semicolon | BLOCKER | BUG |  |
| plsql:LoopUnlabeledEndCheck | "END" statements of labeled loops should be labeled | MAJOR | CODE_SMELL | convention, pitfall |
| plsql:LoopUnlabeledExitCheck | In labeled loops "EXIT" should exit the label | MAJOR | CODE_SMELL | pitfall |
| plsql:LoopUseExitWhenCheck | "EXIT WHEN" should be used rather than "IF ... THEN EXIT; END IF;" | MAJOR | CODE_SMELL | clumsy |
| plsql:LowerCaseReservedWordsCheck | Reserved words should be written in lower case | MINOR | CODE_SMELL | convention |
| plsql:MagicLiteral | Magic literals should not be used | MAJOR | CODE_SMELL | brain-overload |
| plsql:MagicNumber | Magic numbers should not be used | MAJOR | CODE_SMELL | brain-overload |
| plsql:MaskedExceptionCheck | Exceptions should not be ignored | MINOR | CODE_SMELL | cwe, error-handling, suspicious |
| plsql:MlslabelDatatypeUsageCheck | "MLSLABEL" should not be used | MAJOR | BUG | obsolete |
| plsql:MultiLineCommentFormatCheck | Lines in a multiline comment should start with "*" | MINOR | CODE_SMELL | convention |
| plsql:NameReusedInInnerScope | Labels should not be reused in inner scopes | MAJOR | CODE_SMELL | pitfall |
| plsql:NamingConstantsCheck | Constant names should comply with a naming convention | CRITICAL | CODE_SMELL | convention |
| plsql:NamingCursorParametersCheck | Cursor parameters should follow a naming convention | MINOR | CODE_SMELL | convention |
| plsql:NamingCursorsCheck | Cursors should follow a naming convention | MINOR | CODE_SMELL | convention |
| plsql:NamingExceptionsCheck | Exceptions should follow a naming convention | MINOR | CODE_SMELL | convention |
| plsql:NamingFunctionAndProcedureParametersCheck | Function and procedure parameters should comply with a naming convention | MAJOR | CODE_SMELL | convention |
| plsql:NamingObjectAttribute | Object attributes should comply with a naming convention | MINOR | CODE_SMELL | convention |
| plsql:NamingRecordField | Record fields should comply with a naming convention | MINOR | CODE_SMELL | convention |
| plsql:NamingTypesCheck | Types should follow a naming convention | MINOR | CODE_SMELL | convention |
| plsql:NamingVariablesCheck | Variables should comply with a naming convention | MINOR | CODE_SMELL | convention |
| plsql:NaturalJoinUsageCheck | "NATURAL JOIN" queries should not be used | MAJOR | CODE_SMELL | design, sql |
| plsql:NcharByteLengthUsageCheck | "NCHAR" and "NVARCHAR2" size should not be specified in bytes | BLOCKER | BUG |  |
| plsql:NestedCommentsCheck | Comments should not be nested | MINOR | CODE_SMELL | confusing |
| plsql:NestedIf | "IF" statements should not be nested too deeply | CRITICAL | CODE_SMELL | brain-overload |
| plsql:NestedSubqueriesCheck | Nested subqueries should be avoided | MAJOR | CODE_SMELL | performance, sql |
| plsql:NoSonarCheck | Track uses of "NOSONAR" comments | MAJOR | CODE_SMELL | bad-practice |
| plsql:NotNullDeclarationWithoutInitializationCheck | "NOT NULL" variables should be initialized | BLOCKER | BUG |  |
| plsql:Notfound | "cursor%NOTFOUND" should be used instead of "NOT cursor%FOUND" | MINOR | CODE_SMELL | clumsy |
| plsql:NullComparison | "NULL" should not be compared directly | MAJOR | BUG | sql |
| plsql:NumberWithoutPrecisionCheck | "NUMBER" variables should be declared with precision | MAJOR | CODE_SMELL | performance |
| plsql:OneStatementPerLineCheck | Statements should be on separate lines | MAJOR | CODE_SMELL | convention |
| plsql:OracleJoinOperatorUsageCheck | Oracle's join operator (+) should not be used | MINOR | CODE_SMELL | lock-in, sql |
| plsql:OrderByColumnNumberCheck | Column names should be used in a SQL "ORDER BY" clause | MAJOR | CODE_SMELL | sql |
| plsql:OrderByExplicitAscCheck | An "ORDER BY" direction should be specified explicitly | MINOR | CODE_SMELL | confusing, sql |
| plsql:OverridePredefinedExceptionCheck | Predefined exceptions should not be overridden | BLOCKER | BUG |  |
| plsql:ParameterExplicitInCheck | Parameter "IN" mode should be specified explicitly | MINOR | CODE_SMELL | convention |
| plsql:PipelinedFunctionsWithoutPipeRow | Pipelined functions should have at least one "PIPE ROW" statement and not return an expression (PLS-00633) | BLOCKER | BUG |  |
| plsql:PlSql.CreateFunctionAndCreateProcedureDocumented | Procedures and functions should be documented | MAJOR | CODE_SMELL |  |
| plsql:PlSql.FileComplexity | Files should not be too complex | MAJOR | CODE_SMELL |  |
| plsql:PlSql.FunctionAndProcedureComplexity | Functions and procedures should not be too complex | CRITICAL | CODE_SMELL | brain-overload |
| plsql:PlSql.FunctionAndProcedureExcessiveParameters | Functions and procedures should not have too many parameters | MAJOR | CODE_SMELL | brain-overload |
| plsql:PlSql.FunctionAndProcedureNaming | Function and procedure names should comply with a naming convention | MAJOR | CODE_SMELL | convention |
| plsql:PlSql.Goto | "GOTO" statements should not be used | MAJOR | CODE_SMELL | brain-overload |
| plsql:PlSql.PackageNaming | Package names should comply with a naming convention | MINOR | CODE_SMELL | convention |
| plsql:PlSql.ParsingError | Track parsing failures | MAJOR | CODE_SMELL | suspicious |
| plsql:PlSql.UseWhenOthers | "WHEN OTHERS" clauses should be used for exception handling | CRITICAL | CODE_SMELL | cwe, error-handling |
| plsql:PositionalAndNamedArgumentMixCheck | Positional and named arguments should not be mixed in invocations | CRITICAL | BUG |  |
| plsql:PreferExecuteImmediateToDbmsSqlCheck | "EXECUTE IMMEDIATE" should be used instead of DBMS_SQL procedure calls | MAJOR | CODE_SMELL | clumsy |
| plsql:ProcedureWithoutParametersCheck | Procedures should have parameters | MAJOR | CODE_SMELL | design |
| plsql:QuotedIdentifiersCheck | Quoted identifiers should not be used | BLOCKER | CODE_SMELL | pitfall |
| plsql:ReliesOnClauseUsage | The "RELIES_ON" clause should not be used | MINOR | CODE_SMELL | obsolete |
| plsql:ResultCacheHintUsage | The "result_cache" hint should be avoided | MAJOR | BUG |  |
| plsql:ReturnInInitializationSectionCheck | "PACKAGE BODY" initialization sections should not contain "RETURN" statements | MAJOR | BUG | unused |
| plsql:ReturnInLoop | "RETURN" should not be used from within a loop | MAJOR | CODE_SMELL |  |
| plsql:ReturnInProcedureCheck | Procedures should not contain "RETURN" statements | MINOR | CODE_SMELL | brain-overload |
| plsql:RowidAndUrowidCheck | "ROWID" and "UROWID" data types should not be used | MAJOR | CODE_SMELL | lock-in, sql |
| plsql:SelectListSizeCheck | Queries should not "SELECT" too many columns | MAJOR | CODE_SMELL | brain-overload, sql |
| plsql:SelectStarCheck | Columns to be read with a "SELECT" statement should be clearly defined | MAJOR | CODE_SMELL | performance, sql |
| plsql:SimpleIntegerPlsIntegerCheck | "SIMPLE_INTEGER" should be used instead of "PLS_INTEGER" | MAJOR | CODE_SMELL | error-handling, performance |
| plsql:SingleLineCommentsSyntaxCheck | Single line comments should start with "--" | MINOR | CODE_SMELL | convention |
| plsql:SizeConstraintMissingCheck | Size should be specified for string variables | BLOCKER | BUG |  |
| plsql:StandaloneProcAndFuncCheck | Procedures and functions should be encapsulated in packages | MAJOR | CODE_SMELL | brain-overload |
| plsql:SysOwnedFunctions | Sensitive "SYS" owned functions should not be used | CRITICAL | VULNERABILITY | cwe |
| plsql:TablesShouldBeAliasedCheck | Tables should be aliased | MAJOR | CODE_SMELL | brain-overload, sql |
| plsql:TriggerCommitRollbackCheck | "COMMIT" and "ROLLBACK" should not be called from non-autonomous transaction triggers | CRITICAL | BUG |  |
| plsql:TriggerOfConditionsCheck | DML events clauses should not include multiple "OF" clauses | MAJOR | BUG |  |
| plsql:UnionUsageCheck | "UNION" should be used with caution | MAJOR | CODE_SMELL | performance, sql |
| plsql:UnusedLabel | Unused labels should be removed | MAJOR | CODE_SMELL | unused |
| plsql:UpperCaseReservedWordsCheck | Reserved words should be written in upper case | MINOR | CODE_SMELL | convention |
| plsql:UseAnsiJoinsCheck | SQL tables should be joined with the "JOIN" keyword | MINOR | CODE_SMELL | obsolete, sql |
| plsql:UseAsForColumnAliasesCheck | Column aliases should be defined using "AS" | MAJOR | CODE_SMELL | pitfall |
| plsql:UseFetchBulkCollectIntoCheck | "FETCH ... BULK COLLECT INTO" should be used | MAJOR | CODE_SMELL | performance |
| plsql:UseForallStatementCheck | "FORALL" should be used | MAJOR | CODE_SMELL | performance |
| plsql:UseNativeSqlJoinsInsteadOfEmbeddedCursorLoopsCheck | Native SQL joins should be used | MAJOR | CODE_SMELL | performance, sql |
| plsql:VarcharUsageCheck | "VARCHAR2" should be used | MAJOR | CODE_SMELL | lock-in |
| plsql:VariableInPackageSpecificationCheck | Global public variables should not be defined | BLOCKER | CODE_SMELL | design |
| plsql:VariableNotNullUsageCheck | Variables should be nullable | MAJOR | CODE_SMELL | performance |
| plsql:VariableRedeclaration | Variables should be declared only once in a scope | BLOCKER | BUG |  |
| plsql:WeakRefCursorCheck | Weak "REF CURSOR" types should not be used | CRITICAL | CODE_SMELL | design |
| plsql:WhenOthersAsOnlyExceptionHandlerCheck | "WHEN OTHERS" should not be the only exception handler | CRITICAL | CODE_SMELL | cwe, error-handling |
| plsql:XPathCheckPlSql | Track breaches of an XPath rule | MAJOR | CODE_SMELL |  |
