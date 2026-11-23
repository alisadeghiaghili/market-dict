# Python rules — full SonarQube set

Source: codeanalysis.ime.co.ir (SonarQube 2026.4.0), pulled 2026-11-18 via /api/rules/search (language key `py`).
Total: **498** rules. By type: CODE_SMELL=266, VULNERABILITY=97, BUG=135.
By severity: BLOCKER=96, CRITICAL=92, INFO=2, MAJOR=234, MINOR=74.

Every rule below is a hard requirement for new code in this skill. Before writing code that a rule touches, read the rule's full text on the live instance (`GET /api/rules/show?key=<rule>` — see `sonarqube-api.md`); if the instance is unreachable, the rule name and severity here are the guidance.

| Key | Rule | Severity | Type | Tags |
|---|---|---|---|---|
| python:S100 | Method names should comply with a naming convention | MINOR | CODE_SMELL | convention |
| python:S101 | Class names should comply with a naming convention | MINOR | CODE_SMELL | convention |
| python:S104 | Files should not have too many lines of code | MAJOR | CODE_SMELL | brain-overload |
| python:S107 | Functions, methods and lambdas should not have too many parameters | MAJOR | CODE_SMELL | brain-overload |
| python:S108 | Nested blocks of code should not be left empty | MAJOR | CODE_SMELL | suspicious |
| python:S112 | "Exception" and "BaseException" should not be raised | MAJOR | CODE_SMELL | cwe, error-handling |
| python:S113 | Files should end with a newline | MINOR | CODE_SMELL | convention |
| python:S116 | Field names should comply with a naming convention | MINOR | CODE_SMELL | convention |
| python:S117 | Local variable and function parameter names should comply with a naming convention | MINOR | CODE_SMELL | convention |
| python:S125 | Sections of code should not be commented out | MAJOR | CODE_SMELL | unused |
| python:S134 | Control flow statements "if", "for", "while", "try" and "with" should not be nested too deeply | CRITICAL | CODE_SMELL | brain-overload |
| python:S138 | Functions should not have too many lines of code | MAJOR | CODE_SMELL | brain-overload |
| python:S139 | Comments should not be located at the end of lines of code | MINOR | CODE_SMELL | convention |
| python:S905 | Non-empty statements should change control flow or have at least one side-effect | MAJOR | BUG | cwe, unused |
| python:S930 | The number and name of arguments passed to a function should match its parameters | BLOCKER | BUG | cwe |
| python:S935 | Functions and methods should only return expected values | BLOCKER | BUG | cwe, typing |
| python:S1045 | All "except" blocks should be able to catch exceptions | MAJOR | BUG | suspicious |
| python:S1066 | Mergeable "if" statements should be combined | MAJOR | CODE_SMELL | clumsy |
| python:S1110 | Unnecessary parentheses should be removed | MINOR | CODE_SMELL | readability, redundant |
| python:S1128 | Unnecessary imports should be removed | MINOR | CODE_SMELL | convention, unused |
| python:S1131 | Lines should not end with trailing whitespaces | MINOR | CODE_SMELL | convention |
| python:S1134 | Track uses of "FIXME" tags | MAJOR | CODE_SMELL | cwe |
| python:S1135 | Track uses of "TODO" tags | INFO | CODE_SMELL | cwe |
| python:S1142 | Functions should not contain too many return statements | MAJOR | CODE_SMELL | brain-overload |
| python:S1143 | Break, continue and return statements should not occur in "finally" blocks | CRITICAL | BUG | cwe, error-handling, pitfall |
| python:S1144 | Unused class-private methods should be removed | MAJOR | CODE_SMELL | suspicious |
| python:S1172 | Unused function parameters should be removed | MAJOR | CODE_SMELL | unused |
| python:S1186 | Functions and methods should not be empty | CRITICAL | CODE_SMELL | suspicious |
| python:S1192 | String literals should not be duplicated | CRITICAL | CODE_SMELL | design |
| python:S1226 | Function parameters initial values should not be ignored | MINOR | BUG | suspicious |
| python:S1244 | Floating point numbers should not be tested for equality | MAJOR | BUG | pytorch, data-science, numpy, suspicious |
| python:S1309 | Track uses of noqa comments | INFO | CODE_SMELL |  |
| python:S1313 | IP addresses should not be hardcoded | MINOR | CODE_SMELL | bad-practice, former-hotspot |
| python:S1451 | Track lack of copyright and license headers | BLOCKER | CODE_SMELL | convention |
| python:S1481 | Unused local variables should be removed | MINOR | CODE_SMELL | unused |
| python:S1515 | Functions and lambdas should not reference variables defined in enclosing loops | MAJOR | CODE_SMELL | suspicious |
| python:S1542 | Function names should comply with a naming convention | MAJOR | CODE_SMELL | convention, pep |
| python:S1578 | Module names should comply with a naming convention | MINOR | CODE_SMELL | convention |
| python:S1607 | A reason should be provided when skipping a test | MAJOR | CODE_SMELL | tests, bad-practice, confusing |
| python:S1656 | Variables should not be self-assigned | MAJOR | BUG | convention, confusing |
| python:S1700 | A field should not duplicate the name of its containing class | MAJOR | CODE_SMELL | brain-overload |
| python:S1707 | Track "TODO" and "FIXME" comments that do not contain a reference to a person | MINOR | CODE_SMELL | convention |
| python:S1716 | "break" and "continue" should not be used outside a loop | CRITICAL | BUG | pitfall |
| python:S1717 | "\" should only be used as an escape character outside of raw strings | MAJOR | BUG | deprecated |
| python:S1720 | Docstrings should be defined | MAJOR | CODE_SMELL | convention |
| python:S1721 | Parentheses should not be used after certain keywords | MINOR | CODE_SMELL | deprecated |
| python:S1722 | New-style classes should be used | MINOR | CODE_SMELL | python3 |
| python:S1751 | Loops with at most one iteration should be refactored | MAJOR | BUG | bad-practice, confusing |
| python:S1763 | All code should be reachable | MAJOR | BUG | cwe, unused |
| python:S1764 | Identical expressions should not be used on both sides of a binary operator | MAJOR | BUG | suspicious |
| python:S1845 | Methods and field names should not differ only by capitalization | BLOCKER | CODE_SMELL | convention, confusing |
| python:S1854 | Unused assignments should be removed | MAJOR | CODE_SMELL | cwe, unused |
| python:S1862 | Related "if/else if" statements should not have the same condition | MAJOR | BUG | unused, pitfall |
| python:S1871 | Two branches in a conditional structure should not have exactly the same implementation | MAJOR | CODE_SMELL | design, suspicious |
| python:S1940 | Boolean checks should not be inverted | MINOR | CODE_SMELL | pitfall |
| python:S2053 | Password hashing functions should use an unpredictable salt | CRITICAL | VULNERABILITY | cwe |
| python:S2068 | Credentials should not be hard-coded | MAJOR | VULNERABILITY | cwe, secret, former-hotspot |
| python:S2077 | SQL queries should not be dynamically formatted | MAJOR | VULNERABILITY | cwe, bad-practice, former-hotspot, sql |
| python:S2092 | Cookies should have the "secure" flag | MINOR | VULNERABILITY | cwe, fastapi, django, privacy |
| python:S2115 | A secure password should be used when connecting to a database | BLOCKER | VULNERABILITY | cwe, secret |
| python:S2159 | Unnecessary equality checks should not be made | BLOCKER | BUG | suspicious |
| python:S2187 | TestCases should contain tests | BLOCKER | CODE_SMELL | tests, pytest, unittest |
| python:S2190 | Recursion should not be infinite | BLOCKER | BUG | suspicious |
| python:S2201 | Return values from functions without side effects should not be ignored | MAJOR | BUG | confusing, suspicious |
| python:S2208 | Wildcard imports should not be used | CRITICAL | CODE_SMELL | bad-practice, pitfall |
| python:S2245 | Pseudorandom number generators (PRNGs) should not be used in security contexts | MAJOR | VULNERABILITY | cwe, former-hotspot |
| python:S2257 | Custom cryptographic algorithms should not be used | CRITICAL | VULNERABILITY | cwe, bad-practice, former-hotspot |
| python:S2275 | String formatting should not lead to runtime errors | BLOCKER | BUG | pitfall |
| python:S2325 | Methods and properties that don't access instance data should be static | MINOR | CODE_SMELL | pitfall |
| python:S2612 | File permissions should not be set to world-accessible values | MAJOR | VULNERABILITY | cwe, former-hotspot |
| python:S2638 | Method overrides should not change contracts | CRITICAL | CODE_SMELL | suspicious |
| python:S2710 | The first argument to class methods should follow the naming convention | CRITICAL | CODE_SMELL | convention, confusing, pitfall |
| python:S2711 | "yield" and "return" should not be used outside functions | BLOCKER | BUG | syntax, pitfall |
| python:S2712 | "return" with a value should not be used in a generator function | BLOCKER | BUG | python3, syntax, pitfall |
| python:S2733 | "__exit__" should accept type, value, and traceback arguments | BLOCKER | BUG | pitfall |
| python:S2734 | "__init__" should not return a value | BLOCKER | BUG | convention, pitfall |
| python:S2737 | "except" clauses should do more than raise the same issue | MINOR | CODE_SMELL | error-handling, unused, finding, clumsy |
| python:S2755 | XML parsers should not be vulnerable to XXE attacks | BLOCKER | VULNERABILITY | cwe |
| python:S2757 | Non-existent operators like "=+" should not be used | MAJOR | BUG | convention, confusing |
| python:S2761 | Doubled prefix operators "not" and "~" should not be used | MAJOR | CODE_SMELL | confusing |
| python:S2772 | "pass" should not be used needlessly | MINOR | CODE_SMELL | confusing |
| python:S2823 | Only strings should be listed in "__all__" | BLOCKER | BUG | python3 |
| python:S2836 | Loops without "break" should not have "else" clauses | MAJOR | CODE_SMELL | suspicious |
| python:S2876 | "__iter__" should return an iterator | BLOCKER | BUG | python3, pep |
| python:S3329 | Cipher Block Chaining IVs should be unpredictable | CRITICAL | VULNERABILITY | cwe, bad-practice |
| python:S3330 | Cookies should have the "HttpOnly" flag | MINOR | VULNERABILITY | cwe, fastapi, django, privacy |
| python:S3358 | Conditional expressions should not be nested | MAJOR | CODE_SMELL | confusing |
| python:S3403 | Identity operators should not be used with dissimilar types | BLOCKER | BUG | typing, confusing, pitfall |
| python:S3415 | Assertion arguments should be passed in the correct order | MAJOR | CODE_SMELL | tests, suspicious |
| python:S3457 | String formatting should be used correctly | MAJOR | CODE_SMELL | confusing |
| python:S3516 | Functions returns should not be invariant | BLOCKER | CODE_SMELL | design, confusing |
| python:S3626 | Jump statements should not be redundant | MINOR | CODE_SMELL | redundant, clumsy |
| python:S3699 | The output of functions that don't return anything should not be used | MAJOR | BUG | python3 |
| python:S3752 | HTTP routes should restrict allowed HTTP methods | MINOR | VULNERABILITY | cwe, django, former-hotspot |
| python:S3776 | Cognitive Complexity of functions should not be too high | CRITICAL | CODE_SMELL | brain-overload |
| python:S3801 | Functions should use "return" consistently | MAJOR | CODE_SMELL | design, confusing |
| python:S3827 | Variables, classes and functions should be defined before being used | BLOCKER | BUG | python3, pitfall |
| python:S3862 | Iterable unpacking, "for-in" loops and "yield from" should use an Iterable object | BLOCKER | BUG | defign, typing, pitfall |
| python:S3923 | All branches in a conditional structure should not have exactly the same implementation | MAJOR | BUG | convention, suspicious |
| python:S3981 | Collection sizes and array length comparisons should make sense | MAJOR | BUG | confusing |
| python:S3984 | Exceptions should not be created without being raised | MAJOR | BUG | error-handling |
| python:S3985 | Unused private nested classes should be removed | MAJOR | CODE_SMELL | unused |
| python:S4143 | Collection content should not be replaced unconditionally | MAJOR | BUG | suspicious |
| python:S4144 | Functions and methods should not have identical implementations | MAJOR | CODE_SMELL | confusing, duplicate, suspicious |
| python:S4423 | Weak SSL/TLS protocols should not be used | CRITICAL | VULNERABILITY | cwe, privacy |
| python:S4426 | Cryptographic key generation should be based on strong parameters | CRITICAL | VULNERABILITY | cwe, privacy |
| python:S4433 | LDAP connections should be authenticated | CRITICAL | VULNERABILITY | cwe |
| python:S4487 | Unread "private" attributes should be removed | CRITICAL | CODE_SMELL | cwe, unused |
| python:S4502 | CSRF protections should not be disabled | CRITICAL | VULNERABILITY | cwe, django, flask, former-hotspot |
| python:S4507 | Debugging features should not be enabled in production | MINOR | VULNERABILITY | cwe, error-handling, debug, user-experience |
| python:S4790 | Weak hashing algorithms should not be used | CRITICAL | VULNERABILITY | cwe, former-hotspot |
| python:S4828 | OS process signal parameters should be validated | CRITICAL | CODE_SMELL | cwe, former-hotspot |
| python:S4830 | Server certificates should be verified during SSL/TLS connections | CRITICAL | VULNERABILITY | cwe, privacy, ssl |
| python:S5042 | Expanding archive files should not be done without controlling resource consumption | MAJOR | CODE_SMELL | cwe, former-hotspot |
| python:S5122 | Cross-Origin Resource Sharing (CORS) policy should be restricted to trusted origins | MAJOR | VULNERABILITY | cwe, django, flask, former-hotspot |
| python:S5247 | Auto-escaping in HTML template engines should not be disabled | MAJOR | VULNERABILITY | cwe, django, former-hotspot |
| python:S5332 | Clear-text protocols should not be used | MINOR | VULNERABILITY | cwe, former-hotspot |
| python:S5344 | Passwords should not be stored in plaintext or with a fast hashing algorithm | CRITICAL | VULNERABILITY | cwe, spring |
| python:S5361 | `str.replace` should be preferred to `re.sub` | CRITICAL | CODE_SMELL | regex, performance |
| python:S5439 | HTML autoescape mechanism should not be globally disabled | BLOCKER | VULNERABILITY | deprecated |
| python:S5443 | Temporary files should not be created in publicly writable directories | CRITICAL | VULNERABILITY | cwe, former-hotspot |
| python:S5445 | Insecure temporary file creation methods should not be used | CRITICAL | VULNERABILITY | cwe |
| python:S5527 | Server hostnames should be verified during SSL/TLS connections | CRITICAL | VULNERABILITY | cwe, privacy, ssl |
| python:S5542 | Encryption algorithms should be used with secure mode and padding scheme | CRITICAL | VULNERABILITY | cwe, privacy |
| python:S5547 | Cipher algorithms should be robust | CRITICAL | VULNERABILITY | cwe, privacy |
| python:S5549 | Function arguments should be passed only once | BLOCKER | BUG | syntax |
| python:S5603 | Unused scope-limited definitions should be removed | MAJOR | CODE_SMELL | unused |
| python:S5607 | Operators should be used on compatible types | BLOCKER | BUG | typing |
| python:S5632 | Raised Exceptions must derive from BaseException | BLOCKER | BUG | error-handling, python3 |
| python:S5642 | "in" and "not in" operators should be used on objects supporting them | BLOCKER | BUG | python3, design |
| python:S5644 | Item operations should be done on objects supporting them | BLOCKER | BUG | python3, typing |
| python:S5655 | Arguments given to functions should be of an expected type | CRITICAL | CODE_SMELL | typing, suspicious |
| python:S5659 | JWT should be signed and verified | CRITICAL | VULNERABILITY | cwe, privacy |
| python:S5685 | Walrus operator should not make code confusing | MINOR | CODE_SMELL | bad-practice, pep, confusing |
| python:S5704 | Bare "raise" statements should not be used in "finally" blocks | CRITICAL | CODE_SMELL | error-handling, unpredictable, confusing |
| python:S5706 | Special method "__exit__" should not re-raise the provided exception | MAJOR | CODE_SMELL | error-handling, bad-practice |
| python:S5707 | Exceptions' "__cause__" should be either an Exception or None | CRITICAL | BUG | error-handling, design, pep |
| python:S5708 | Caught Exceptions must derive from BaseException | BLOCKER | BUG | error-handling, design, pep |
| python:S5709 | Custom Exception classes should inherit from "Exception" or one of its subclasses | CRITICAL | CODE_SMELL | convention, bad-practice |
| python:S5712 | Some special methods should return "NotImplemented" instead of raising "NotImplementedError" | CRITICAL | CODE_SMELL | error-handling, bad-practice |
| python:S5713 | A subclass should not be in the same "except" statement as a parent class | MINOR | CODE_SMELL | error-handling, bad-practice, unused |
| python:S5714 | Boolean expressions of exceptions should not be used in "except" statements | BLOCKER | BUG | error-handling, bad-practice |
| python:S5717 | Function parameters' default values should not be modified or assigned | CRITICAL | CODE_SMELL | bad-practice, pitfall |
| python:S5719 | Instance and class methods should have at least one positional parameter | BLOCKER | BUG | python3, syntax |
| python:S5720 | "self" should be the first argument to instance methods | CRITICAL | CODE_SMELL | convention, confusing, suspicious |
| python:S5722 | Special methods should have an expected number of parameters | BLOCKER | BUG | design, bad-practice |
| python:S5724 | Property getter, setter and deleter methods should have the expected number of parameters | BLOCKER | BUG | design, bad-practice |
| python:S5727 | Comparison to None should not be constant | CRITICAL | CODE_SMELL | suspicious |
| python:S5747 | Bare "raise" statements should only be used in "except" blocks | CRITICAL | CODE_SMELL | error-handling, unpredictable, confusing |
| python:S5754 | "SystemExit" should be re-raised | CRITICAL | CODE_SMELL | error-handling, bad-practice, suspicious |
| python:S5756 | Calls should not be made to non-callable values | BLOCKER | BUG | typing |
| python:S5778 | Only one method invocation is expected when testing runtime exceptions | MAJOR | CODE_SMELL | tests, pytest, unittest |
| python:S5779 | Assertions should not be made within the try block of a try-except catching AssertionError | CRITICAL | BUG | tests, pytest, unittest, assertpy |
| python:S5780 | Expressions creating dictionaries should not have duplicate keys | MAJOR | CODE_SMELL | confusing, suspicious |
| python:S5781 | Expressions creating sets should not have duplicate values | MAJOR | CODE_SMELL | suspicious |
| python:S5795 | Identity comparisons should not be used with cached types | MAJOR | CODE_SMELL | suspicious |
| python:S5796 | New objects should not be created only to check their identity | MAJOR | BUG | suspicious |
| python:S5797 | Constants should not be used as conditions | CRITICAL | CODE_SMELL | suspicious |
| python:S5799 | Implicit string and byte concatenations should not be confusing | MAJOR | CODE_SMELL | confusing, suspicious |
| python:S5806 | Builtins should not be shadowed by local variables | MAJOR | CODE_SMELL | bad-practice, confusing, pitfall |
| python:S5807 | Only defined names should be listed in "__all__" | BLOCKER | BUG | design |
| python:S5828 | The "open" builtin function should be called with a valid mode | BLOCKER | BUG | python3, pitfall |
| python:S5842 | Repeated patterns in regular expressions should not match the empty string | MINOR | BUG | regex |
| python:S5843 | Regular expressions should not be too complicated | MAJOR | CODE_SMELL | regex |
| python:S5845 | Assertions comparing incompatible types should not be made | CRITICAL | BUG | tests, typing |
| python:S5850 | Alternatives in regular expressions should be grouped when used with anchors | MAJOR | BUG | regex |
| python:S5852 | Regular expressions should not cause catastrophic backtracking | CRITICAL | VULNERABILITY | cwe, regex, former-hotspot |
| python:S5855 | Regex alternatives should not be redundant | MAJOR | BUG | regex |
| python:S5856 | Regular expressions should be syntactically valid | CRITICAL | BUG | regex |
| python:S5857 | Character classes should be preferred over reluctant quantifiers in regular expressions | MINOR | CODE_SMELL | regex |
| python:S5860 | Names of regular expressions named groups should be used | MAJOR | CODE_SMELL | regex |
| python:S5863 | Assertions should not be given twice the same argument | MAJOR | BUG | tests |
| python:S5864 | Type checks shouldn't be confusing | MAJOR | CODE_SMELL | typing, confusing |
| python:S5868 | Unicode Grapheme Clusters should be avoided inside regex character classes | MAJOR | BUG | regex |
| python:S5869 | Character classes in regular expressions should not contain the same character twice | MAJOR | CODE_SMELL | regex |
| python:S5886 | Function return types should be consistent with their type hint | MAJOR | CODE_SMELL | typing |
| python:S5890 | Values assigned to variables should match their type annotations | MAJOR | CODE_SMELL | typing, confusing |
| python:S5899 | Test methods should be discoverable | MAJOR | CODE_SMELL | tests, unittest, unused |
| python:S5905 | Assert should not be called on a tuple literal | BLOCKER | BUG | tests |
| python:S5906 | The most specific "unittest" assertion should be used | MINOR | CODE_SMELL | tests, unittest |
| python:S5914 | Assertions should not fail or succeed unconditionally | MAJOR | CODE_SMELL | tests, confusing, suspicious |
| python:S5915 | Assertions should not be made at the end of blocks expecting an exception | CRITICAL | BUG | tests, unused, pitfall |
| python:S5918 | Tests should be skipped explicitly | MINOR | CODE_SMELL | tests, bad-practice |
| python:S5953 | Variables, classes and functions should be either defined or imported | BLOCKER | BUG | suspicious |
| python:S5958 | Tests should check which exception is thrown | MAJOR | CODE_SMELL | tests |
| python:S5976 | Similar tests should be grouped in a single Parameterized test | MAJOR | CODE_SMELL | tests, bad-practice, clumsy |
| python:S5994 | Regex patterns following a possessive quantifier should not always fail | CRITICAL | BUG | regex |
| python:S5996 | Regex boundaries should not be used in a way that can never be matched | CRITICAL | BUG | regex |
| python:S6001 | Back references in regular expressions should only refer to capturing groups that are matched before the reference | CRITICAL | BUG | regex |
| python:S6002 | Regex lookahead assertions should not be contradictory | CRITICAL | BUG | regex |
| python:S6019 | Reluctant quantifiers in regular expressions should be followed by an expression that can't match the empty string | MAJOR | CODE_SMELL | regex |
| python:S6035 | Single-character alternations in regular expressions should be replaced with character classes | MAJOR | CODE_SMELL | regex |
| python:S6243 | Reusable resources should be initialized at construction time of Lambda functions | MAJOR | CODE_SMELL | aws |
| python:S6246 | Lambdas should not invoke other lambdas synchronously | MINOR | CODE_SMELL | aws |
| python:S6249 | S3 buckets should enforce HTTPS-only access | MINOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6252 | Amazon S3 buckets should have versioning enabled | MINOR | VULNERABILITY | aws, former-hotspot |
| python:S6262 | AWS region should not be set with a hardcoded String | MINOR | CODE_SMELL | aws |
| python:S6265 | S3 buckets should not grant access to all users or authenticated users | BLOCKER | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6270 | AWS resource-based policies should not grant public access | BLOCKER | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6275 | EBS volumes should be encrypted | MAJOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6281 | Amazon S3 bucket public access should be fully blocked | CRITICAL | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6302 | Policies should not grant all privileges | BLOCKER | VULNERABILITY | cwe, gcp, aws, former-hotspot |
| python:S6303 | Amazon RDS resources should be encrypted at rest | MAJOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6304 | IAM policies should not grant access to all account resources | BLOCKER | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6308 | OpenSearch domains should have encryption at rest enabled | MAJOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6317 | AWS IAM policies should limit the scope of permissions given | CRITICAL | VULNERABILITY | cwe, aws |
| python:S6319 | SageMaker notebook instances should be encrypted at rest | MAJOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6321 | Administration services access should be restricted to specific IP addresses | MINOR | VULNERABILITY | cwe, aws |
| python:S6323 | Alternation in regular expressions should not contain empty alternatives | MAJOR | BUG | regex |
| python:S6326 | Regular expressions should not contain multiple spaces | MAJOR | CODE_SMELL | regex |
| python:S6327 | Amazon SNS topics should be encrypted at rest | MINOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6328 | Replacement strings should reference existing regular expression groups | MAJOR | BUG | regex |
| python:S6329 | Public network access to cloud resources should be disabled | BLOCKER | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6330 | SQS queues should be encrypted | MAJOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6331 | Regular expressions should not contain empty groups | MAJOR | CODE_SMELL | regex |
| python:S6332 | Amazon EFS file systems should be encrypted | MAJOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6333 | AWS API Gateway should require authentication | BLOCKER | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6353 | Regular expression quantifiers and character classes should be used concisely | MINOR | CODE_SMELL | regex |
| python:S6377 | XML signatures should be validated securely | MAJOR | VULNERABILITY |  |
| python:S6395 | Non-capturing groups without quantifier should not be used | MAJOR | CODE_SMELL | regex |
| python:S6396 | Superfluous curly brace quantifiers should be avoided | MAJOR | CODE_SMELL | regex |
| python:S6397 | Character classes in regular expressions should not contain only one character | MAJOR | CODE_SMELL | regex |
| python:S6418 | Secrets should not be hard-coded | BLOCKER | VULNERABILITY | cwe, secret, former-hotspot |
| python:S6437 | Credentials should not be hard-coded | BLOCKER | VULNERABILITY | cwe, secret |
| python:S6463 | Security groups should not allow unrestricted outbound traffic | MAJOR | VULNERABILITY | cwe, aws, former-hotspot |
| python:S6468 | ExceptionGroup and BaseExceptionGroup should not be caught with except* | MAJOR | BUG | error-handling, python3 |
| python:S6537 | Octal escape sequences should not be used in regular expressions | MAJOR | CODE_SMELL | regex, confusing |
| python:S6538 | Function returns should have type hints | MAJOR | CODE_SMELL | convention, typing |
| python:S6540 | Function parameters should have type hints | MAJOR | CODE_SMELL | convention, typing |
| python:S6542 | Any should not be used as a type hint | MAJOR | CODE_SMELL | convention, typing, bad-practice |
| python:S6543 | Type hints of generic types should specify their type parameters | MAJOR | CODE_SMELL | convention, typing |
| python:S6545 | Built-in generic types should be preferred over the typing module in type hints | MINOR | CODE_SMELL | convention, typing |
| python:S6546 | Union type expressions should be preferred over "typing.Union" in type hints | MAJOR | CODE_SMELL | typing |
| python:S6552 | The '@receiver' (Django) and '@route' (Flask) decorators should be the outermost decorators | MAJOR | BUG | django, flask, pitfall |
| python:S6553 | 'null=True' should not be used on string-based fields in Django models | MAJOR | CODE_SMELL | django |
| python:S6554 | Django models should define a "__str__" method | MAJOR | CODE_SMELL | django |
| python:S6556 | "locals()" should not be passed to a Django "render()" function | MAJOR | CODE_SMELL | django |
| python:S6559 | Fields of a Django ModelForm should be defined explicitly | MAJOR | CODE_SMELL | django |
| python:S6560 | The "safe" flag should be set to "False" when serializing non-dictionary objects in Django JSON-encoded responses. | MAJOR | BUG | django |
| python:S6659 | 'startswith' or 'endswith' methods should be used instead of string slicing in condition expressions | MINOR | CODE_SMELL | convention, pep |
| python:S6660 | "isinstance()" should be preferred to direct type comparisons | MINOR | CODE_SMELL | typing |
| python:S6661 | Assignments of lambdas to variables should be replaced by function definitions | MINOR | CODE_SMELL |  |
| python:S6662 | Set members and dictionary keys should be hashable | MAJOR | BUG |  |
| python:S6663 | Sequence indexes must have an __index__ method | MAJOR | BUG |  |
| python:S6709 | Results that depend on random number generation should be reproducible | MAJOR | CODE_SMELL | scientific-computing, data-science, numpy |
| python:S6711 | numpy.random.Generator should be preferred to numpy.random.RandomState | MAJOR | CODE_SMELL | data-science, numpy |
| python:S6714 | Passing a list to np.array should be preferred over passing a generator | MAJOR | CODE_SMELL | data-science, numpy |
| python:S6725 | Equality checks should not be made against "numpy.nan" | BLOCKER | BUG | numpy |
| python:S6727 | The abs_tol parameter should be provided when using math.isclose to compare values to 0 | CRITICAL | BUG | scientific-computing |
| python:S6729 | np.nonzero should be preferred over np.where when only the condition parameter is set | CRITICAL | CODE_SMELL | data-science, numpy |
| python:S6730 | Deprecated NumPy aliases of built-in types should not be used | MAJOR | CODE_SMELL | data-science, numpy |
| python:S6734 | inplace=True should not be used when modifying a Pandas DataFrame | CRITICAL | CODE_SMELL | pandas, data-science |
| python:S6735 | When using pandas.merge or pandas.join, the parameters on, how and validate should be provided | MAJOR | CODE_SMELL | pandas, data-science |
| python:S6740 | 'dtype' parameter should be provided when using 'pandas.read_csv' or 'pandas.read_table' | MAJOR | CODE_SMELL | pandas, data-science |
| python:S6741 | The "pandas.DataFrame.to_numpy()" method should be preferred to the "pandas.DataFrame.values" attribute | MAJOR | CODE_SMELL | pandas, data-science, numpy |
| python:S6742 | pandas.pipe method should be preferred over long chains of instructions | MAJOR | CODE_SMELL | pandas, data-science |
| python:S6779 | Flask secret keys should not be disclosed | BLOCKER | VULNERABILITY | cwe, flask |
| python:S6781 | JWT secret keys should not be disclosed | BLOCKER | VULNERABILITY | cwe, secret |
| python:S6785 | GraphQL queries should not be vulnerable to Denial of Service attacks | CRITICAL | VULNERABILITY | denial-of-service, graphql |
| python:S6786 | GraphQL introspection should be disabled in production | MAJOR | VULNERABILITY | cwe, graphql |
| python:S6792 | Generic classes should be defined using the type parameter syntax | MAJOR | CODE_SMELL | typing |
| python:S6794 | Type aliases should be declared with a "type" statement | MAJOR | CODE_SMELL | typing |
| python:S6795 | Generic type statements should not use "TypeVars" | MAJOR | CODE_SMELL | typing |
| python:S6796 | Generic functions should be defined using the type parameter syntax | MAJOR | CODE_SMELL | typing |
| python:S6799 | "f-strings" should not be nested too deeply | MAJOR | CODE_SMELL |  |
| python:S6863 | Flask error handlers should set HTTP status code | MAJOR | BUG | best-practice, flask |
| python:S6882 | Constructor attributes of date and time objects should be in the range of possible values | CRITICAL | CODE_SMELL | datetime |
| python:S6883 | The 12-hour format should be used with the AM/PM marker, otherwise the 24-hour format should be used | CRITICAL | CODE_SMELL | datetime |
| python:S6887 | "pytz.timezone" should not be passed to the "datetime.datetime" constructor | CRITICAL | CODE_SMELL | datetime |
| python:S6890 | "zoneinfo" should be preferred to "pytz" when using Python 3.9 and later | CRITICAL | CODE_SMELL | datetime |
| python:S6894 | Dates should be formatted correctly when using "pandas.to_datetime" with "dayfirst" or "yearfirst" arguments | CRITICAL | CODE_SMELL | pandas, datetime |
| python:S6900 | Numpy weekmask should have a valid value | CRITICAL | CODE_SMELL | datetime, numpy |
| python:S6903 | Using timezone-aware "datetime" objects should be preferred over using "datetime.datetime.utcnow" and "datetime.datetime.utcfromtimestamp" | CRITICAL | CODE_SMELL | datetime, pitfall |
| python:S6908 | "tensorflow.function" should not be recursive | MAJOR | CODE_SMELL | machine-learning, tensorflow |
| python:S6911 | "tf.function" should not depend on global or free Python variables | MAJOR | CODE_SMELL | machine-learning, tensorflow |
| python:S6918 | "tf.Variable" objects should be singletons when created inside of a "tf.function" | MAJOR | CODE_SMELL | machine-learning, tensorflow |
| python:S6919 | The "input_shape" parameter should not be specified for "tf.keras.Model" subclasses | MAJOR | CODE_SMELL | machine-learning, tensorflow |
| python:S6925 | The "validate_indices" argument should not be set for "tf.gather" function call | MAJOR | CODE_SMELL | machine-learning, tensorflow |
| python:S6928 | Python side effects should not be used inside a "tf.function" | CRITICAL | CODE_SMELL | machine-learning, tensorflow |
| python:S6929 | The reduction axis/dimension should be specified when using reduction operations | MAJOR | CODE_SMELL | machine-learning, tensorflow, scientific-computing, pytorch |
| python:S6965 | REST API actions should be annotated with an HTTP verb attribute | MAJOR | CODE_SMELL | flask |
| python:S6969 | "memory" parameter should be specified for Scikit-Learn Pipeline | MINOR | CODE_SMELL | machine-learning, scikit-learn |
| python:S6971 | Transformers should not be accessed directly when a Scikit-Learn Pipeline uses caching | CRITICAL | BUG | machine-learning, scikit-learn |
| python:S6972 | Nested estimator parameters modification in a Pipeline should refer to valid parameters | MAJOR | CODE_SMELL | machine-learning, scikit-learn |
| python:S6973 | Important hyperparameters should be specified for machine learning libraries' estimators and optimizers | MAJOR | CODE_SMELL | machine-learning, scikit-learn, pytorch |
| python:S6974 | Subclasses of Scikit-Learn's "BaseEstimator" should not set attributes ending with "_" in the "__init__" method | CRITICAL | CODE_SMELL | machine-learning, scikit-learn |
| python:S6978 | Subclasses of "torch.nn.Module" should call the initializer | MAJOR | BUG | machine-learning, pytorch |
| python:S6979 | "torch.tensor" should be used instead of "torch.autograd.Variable" | MAJOR | CODE_SMELL | machine-learning, pytorch |
| python:S6982 | "model.eval()" or "model.train()" should be called after loading the state of a PyTorch model | MAJOR | CODE_SMELL | machine-learning, pytorch |
| python:S6983 | The "num_workers" parameter should be specified for "torch.utils.data.DataLoader" | MINOR | CODE_SMELL | machine-learning, pytorch |
| python:S6984 | Einops pattern should be valid | CRITICAL | BUG | convention, scientific-computing, pitfall |
| python:S6985 | Models should not be loaded with "torch.load" without restricting deserialization | CRITICAL | VULNERABILITY | cwe, machine-learning, pytorch, former-hotspot |
| python:S7483 | Asynchronous functions should not accept timeout parameters | MAJOR | CODE_SMELL | async, trio, asyncio, anyio |
| python:S7484 | Events should be used instead of `sleep` in asynchronous loops | MAJOR | CODE_SMELL | async, trio, asyncio, anyio |
| python:S7486 | Long sleep durations should use sleep_forever() instead of arbitrary intervals | MINOR | CODE_SMELL | async, trio, asyncio, anyio |
| python:S7487 | Async functions should not contain synchronous subprocess calls | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7488 | Use non-blocking sleep functions in asynchronous code | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7489 | Async functions should not contain synchronous OS calls | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7490 | Cancellation scopes should contain checkpoints | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7491 | Checkpoints should be used instead of sleep(0) | MINOR | CODE_SMELL | async, trio, anyio |
| python:S7492 | List comprehensions should not be used with "any()" or "all()" | MINOR | CODE_SMELL |  |
| python:S7493 | Async functions should not contain synchronous file operations | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7494 | Comprehensions should be used instead of constructors around generator expressions | MINOR | CODE_SMELL |  |
| python:S7496 | Creation of collections with literals or comprehensions should not be wrapped in type constructors | MINOR | CODE_SMELL |  |
| python:S7497 | Cancellation exceptions should be re-raised after cleanup | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7498 | Literal syntax should be preferred when creating empty collections or dictionaries with keyword arguments | MINOR | CODE_SMELL |  |
| python:S7499 | Async functions should not contain synchronous HTTP client calls | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7500 | Comprehensions only used to copy should be replaced with the respective constructor calls | MINOR | CODE_SMELL |  |
| python:S7501 | Async functions should not contain input() calls | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7502 | Asyncio tasks should be saved to prevent premature garbage collection | MAJOR | BUG | async, asyncio, pitfall |
| python:S7503 | Async functions should use async features | MINOR | CODE_SMELL | async |
| python:S7504 | When iterating over an iterable object, using "list()" should be avoided | MINOR | CODE_SMELL |  |
| python:S7505 | Generators and comprehensions should be preferred over the usage of "map" and "lambda" when creating collection | MAJOR | CODE_SMELL |  |
| python:S7506 | Dictionary comprehension should not use a static key | CRITICAL | CODE_SMELL |  |
| python:S7507 | "defaultdict" should not be initialized with "default_factory" as a keyword argument | MAJOR | CODE_SMELL |  |
| python:S7508 | Redundant collection functions should be avoided | MINOR | CODE_SMELL |  |
| python:S7510 | The "sorted" function call should not be passed to the "reversed" function as an argument | MAJOR | CODE_SMELL |  |
| python:S7511 | Passing a reversed iterable to "set()", "sorted()", or "reversed()" should be avoided | MAJOR | CODE_SMELL |  |
| python:S7512 | Using ".items()" to iterate over a dictionary should be avoided if possible. | MAJOR | CODE_SMELL |  |
| python:S7513 | TaskGroup/Nursery should not be used for a single start call | MINOR | CODE_SMELL | async, trio, asyncio, anyio |
| python:S7514 | Control flow statements should not be used inside TaskGroup or Nursery blocks | MAJOR | BUG | async, trio, asyncio, anyio |
| python:S7515 | "async with" should be used for asynchronous resource management | MAJOR | BUG | async |
| python:S7516 | "sorted" should not be wrapped directly inside "set" | MINOR | CODE_SMELL |  |
| python:S7517 | Iteration over a dictionary key value pairs should be done with the items() method call | MAJOR | CODE_SMELL |  |
| python:S7519 | Populating a dictionary with a constant value should be done with dict.fromkeys() method call | MINOR | CODE_SMELL |  |
| python:S7608 | S3 operations should verify bucket ownership using ExpectedBucketOwner parameter | MAJOR | VULNERABILITY | s3, aws |
| python:S7609 | AWS CloudWatch metrics namespace should not begin with `AWS/` | MAJOR | CODE_SMELL | aws |
| python:S7613 | AWS Lambda handlers should return only JSON serializable values | MAJOR | BUG |  |
| python:S7614 | AWS Lambda handlers must not be an async function | MINOR | CODE_SMELL |  |
| python:S7617 | Reserved environment variable names should not be overridden in Lambda functions | MAJOR | CODE_SMELL | aws |
| python:S7618 | Network calls in AWS Lambda functions shouldn't be made without explicit timeout parameters | MAJOR | BUG | aws |
| python:S7619 | "botocore.exceptions.ClientError" should be explicitly caught and handled | MAJOR | CODE_SMELL | aws |
| python:S7620 | AWS Lambda handlers should clean up temporary files in /tmp directory | MAJOR | BUG | lambda, aws |
| python:S7621 | AWS waiters should be used instead of custom polling loops | MAJOR | CODE_SMELL | aws |
| python:S7622 | boto3 operations that support pagination should be performed using paginators or manual pagination handling | MAJOR | CODE_SMELL | aws |
| python:S7625 | Long-term AWS access keys should not be used directly in code | BLOCKER | VULNERABILITY | aws |
| python:S7632 | Issue suppression comment should have the correct format | MAJOR | CODE_SMELL |  |
| python:S7931 | "NotImplemented" should not be used in boolean contexts | BLOCKER | BUG | python3.14 |
| python:S7941 | Compression modules should be imported from the compression namespace | MINOR | CODE_SMELL | python3.14 |
| python:S7942 | Template strings should be processed before use | BLOCKER | BUG | python3.14 |
| python:S7943 | Template and str should not be concatenated directly | BLOCKER | BUG | python3.14 |
| python:S7945 | Template string processing should use structural pattern matching | MAJOR | CODE_SMELL |  |
| python:S8370 | Query parameters should not be used in Flask POST requests | CRITICAL | CODE_SMELL | flask |
| python:S8371 | HTTP headers should be accessed safely to avoid KeyError exceptions | BLOCKER | BUG | error-handling, flask |
| python:S8374 | Flask class-based view decorators should be applied using the "decorators" attribute | BLOCKER | BUG | decorator, flask |
| python:S8375 | Flask "preprocess_request()" return values should be handled | BLOCKER | BUG | flask |
| python:S8385 | "send_file" should specify "mimetype" or "download_name" when used with file-like objects | BLOCKER | BUG | web, flask |
| python:S8389 | FastAPI file upload endpoints should use "Form()" with Pydantic validators instead of "Body()" or "Depends()" | BLOCKER | VULNERABILITY | fastapi, file-upload, pydantic |
| python:S8392 | Web servers should not bind to all network interfaces | BLOCKER | VULNERABILITY | fastapi, least-privilege, uvicorn, flask |
| python:S8396 | Optional Pydantic fields should have explicit default values | CRITICAL | CODE_SMELL | pydantic, type-hint, validation |
| python:S8397 | FastAPI applications should be passed as import strings when using reload, debug, or workers | BLOCKER | CODE_SMELL | fastapi, uvicorn, pitfall |
| python:S8400 | Endpoints returning 204 status should have an empty response body | BLOCKER | BUG | fastapi, http, api |
| python:S8401 | Child routers should be included before parent router registration | BLOCKER | BUG | fastapi, router, api |
| python:S8405 | TestClient requests should use "content" parameter for bytes or text | BLOCKER | CODE_SMELL | httpx, fastapi, tests, starlette |
| python:S8409 | FastAPI routes should not specify redundant "response_model" parameters | MINOR | CODE_SMELL | fastapi, api, redundant |
| python:S8410 | FastAPI dependencies should use "Annotated" type hints | MINOR | CODE_SMELL | convention, fastapi, type-hint |
| python:S8411 | FastAPI path parameters should be included in route function signatures | BLOCKER | BUG | fastapi, api, pitfall |
| python:S8412 | Generic route decorators should not be used | MINOR | CODE_SMELL | convention, fastapi, readability |
| python:S8413 | Router prefixes should be defined during "APIRouter" initialization | BLOCKER | CODE_SMELL | convention, fastapi, readability |
| python:S8414 | CORSMiddleware should be added last in the middleware chain | BLOCKER | CODE_SMELL | fastapi, cors, configuration, middleware |
| python:S8415 | HTTPException responses should be documented in endpoint metadata | MAJOR | CODE_SMELL | fastapi, openapi, documentation |
| python:S8490 | Enum classes should not be decorated with "@dataclass" | BLOCKER | BUG | enum, pitfall |
| python:S8492 | "set.discard()" should be used instead of checking membership before removal | MINOR | CODE_SMELL | performance, pythonic, idiom |
| python:S8493 | "StopIteration" should not be raised inside generators | BLOCKER | BUG | python3, pitfall |
| python:S8494 | Attributes should only be assigned if they are declared in "__slots__" | BLOCKER | BUG | slots, pitfall |
| python:S8495 | Functions should return tuples of consistent length | MAJOR | CODE_SMELL | type-system, api-design, pitfall |
| python:S8500 | Comparison methods should be defined completely | MAJOR | CODE_SMELL | comparison, pitfall |
| python:S8502 | "set.update()" should be used instead of a for-loop with "add()" | MINOR | CODE_SMELL | performance, pythonic, idiom |
| python:S8503 | Membership tests should not use empty collections | MAJOR | BUG | suspicious, pitfall |
| python:S8504 | Property methods should have a return statement | MAJOR | BUG | pitfall |
| python:S8505 | "@singledispatch" and "@singledispatchmethod" should not be confused | BLOCKER | BUG | confusing, pitfall |
| python:S8507 | TypeVar, ParamSpec, and NewType names should match their assigned variable names | MAJOR | CODE_SMELL | convention, readability, type-hint |
| python:S8508 | Mutable default values should not be used with "dict.fromkeys()" or "ContextVar()" | BLOCKER | BUG | concurrency, pitfall |
| python:S8509 | Classes should not inherit from the same base class multiple times | CRITICAL | CODE_SMELL | confusing, pitfall |
| python:S8510 | Loop variables should not be reused in nested loops | CRITICAL | CODE_SMELL | confusing, pitfall |
| python:S8511 | Multiple inheritance should not create Method Resolution Order (MRO) conflicts | BLOCKER | BUG | design, inheritance, pitfall |
| python:S8512 | Class fields should not be defined multiple times | CRITICAL | CODE_SMELL | confusing, dead-code, pitfall |
| python:S8513 | "startswith" and "endswith" calls should use tuples instead of multiple "or" operators | MAJOR | CODE_SMELL | performance, pythonic |
| python:S8514 | Dataclass attributes should use type annotations | MAJOR | CODE_SMELL | confusing, pitfall |
| python:S8515 | TypeVars should not be both covariant and contravariant | BLOCKER | BUG | type, pitfall |
| python:S8516 | Group iterators from "itertools.groupby" should not be reused | MAJOR | BUG | confusing, pitfall |
| python:S8517 | "sorted()" should not be used with indexing to find minimum or maximum values | MAJOR | CODE_SMELL | performance, pythonic |
| python:S8518 | "enumerate()" values should be unpacked instead of using index lookups | MAJOR | CODE_SMELL | readability, performance, pythonic |
| python:S8519 | "list(...)[0]" should not be used to get the first element | MAJOR | CODE_SMELL | performance, pythonic |
| python:S8520 | "sum()" should not be used with an empty list to concatenate lists | MAJOR | CODE_SMELL | performance, pitfall |
| python:S8521 | Dictionary membership tests should not explicitly call ".keys()" | MINOR | CODE_SMELL | pythonic, idiom |
| python:S8554 | Logging statements should follow Python best practices | MAJOR | CODE_SMELL | convention, performance, pitfall |
| python:S8572 | "logging.exception()" should be used instead of "logging.error()" in exception handlers | MAJOR | CODE_SMELL | exception, logging |
| python:S8685 | Mutable or stateful values should not be used as default values in dataclass attributes | MAJOR | BUG | dataclass, pitfall |
| python:S8714 | Dedicated exception assertions should be used instead of "try-except" with "fail()" | MINOR | CODE_SMELL | tests |
| python:S8786 | Regular expressions should not cause non-linear backtracking | MAJOR | CODE_SMELL | regex, performance |
| python:S8900 | Deprecated Beautiful Soup methods should be replaced with their modern equivalents | MAJOR | CODE_SMELL | convention, pythonic, deprecated |
| python:S8903 | HTML elements should be created with "new_tag()" instead of inserting raw HTML strings | MAJOR | CODE_SMELL | html, api, pitfall |
| python:S8904 | BeautifulSoup elements should be checked for None before accessing | CRITICAL | BUG | web, beautifulsoup, pitfall |
| python:S8905 | BeautifulSoup parser should be explicitly specified | MAJOR | CODE_SMELL | unpredictable, html, pitfall |
| python:S8906 | CSS selectors should be used when selecting elements with multiple required classes | MAJOR | BUG | css, confusing, pitfall |
| python:S8963 | Pydantic models should not use multiple inheritance with conflicting configurations | MAJOR | CODE_SMELL | pydantic, confusing, pitfall |
| python:S8966 | pydantic-core serialization calls should provide fallback handlers | CRITICAL | BUG | serialization, pydantic, pitfall |
| python:S8971 | "SkipValidation" should not be combined with validation constraints | MINOR | BUG | pydantic, type-hint, pitfall |
| python:S8973 | Double leading underscores should not be used for private attributes in Pydantic models | CRITICAL | BUG | pydantic, pitfall |
| python:S8974 | "json_schema_input_type" should not be used with "mode='after'" field validators | CRITICAL | BUG | pydantic, pitfall |
| python:BackticksUsage | Backticks should not be used | BLOCKER | CODE_SMELL | python3 |
| python:ClassComplexity | Cyclomatic Complexity of classes should not be too high | CRITICAL | CODE_SMELL | brain-overload |
| python:CommentRegularExpression | Track comments matching a regular expression | MAJOR | CODE_SMELL | convention |
| python:ExecStatementUsage | The "exec" statement should not be used | BLOCKER | CODE_SMELL | python3, obsolete |
| python:FileComplexity | Files should not be too complex | MAJOR | CODE_SMELL | brain-overload |
| python:FunctionComplexity | Cyclomatic Complexity of functions should not be too high | CRITICAL | CODE_SMELL | brain-overload |
| python:InequalityUsage | "<>" should not be used to test inequality | MAJOR | CODE_SMELL | obsolete |
| python:LineLength | Lines should not be too long | MAJOR | CODE_SMELL | convention |
| python:LongIntegerWithLowercaseSuffixUsage | Long suffix "L" should be upper case | MINOR | CODE_SMELL | convention |
| python:NoSonar | Track uses of "NOSONAR" comments | MAJOR | CODE_SMELL | bad-practice |
| python:OneStatementPerLine | Statements should be on separate lines | MAJOR | CODE_SMELL | convention |
| python:ParsingError | Python parser failure | MAJOR | CODE_SMELL | suspicious |
| python:PreIncrementDecrement | Increment and decrement operators should not be used | MAJOR | BUG | convention |
| python:PrintStatementUsage | The "print" statement should not be used | MAJOR | CODE_SMELL | python3, obsolete |
| pythonarchitecture:S7788 | Relationships should align with the intended architecture | MAJOR | CODE_SMELL | architecture-deviation, architecture |
| pythonarchitecture:S7789 | Files should be located according to the intended architecture | MAJOR | CODE_SMELL | architecture-deviation, architecture |
| pythonarchitecture:S8134 | Forbidden relationships should be removed to solve tangles as directed by the project's architect | MAJOR | CODE_SMELL | architecture-directive, architecture |
| pythonarchitecture:S8464 | Intended architecture components should be implemented | MAJOR | CODE_SMELL | architecture-deviation, architecture |
| pythonarchitecture:S8483 | Architecture directive to rename a component should be applied | MAJOR | CODE_SMELL | architecture-directive, architecture |
| pythonarchitecture:S8484 | Architecture directive to move a component should be applied | MAJOR | CODE_SMELL | architecture-directive, architecture |
| pythonarchitecture:S8487 | Relationships should align with the interface design of the intended architecture | MAJOR | CODE_SMELL | architecture-deviation, architecture |
| pythonbugs:S2259 | Attributes should not be accessed on "None" values | MAJOR | BUG | cwe |
| pythonbugs:S2583 | Conditionally executed code should be reachable | MAJOR | BUG | cwe, unused, suspicious, pitfall |
| pythonbugs:S2589 | Boolean expressions should not be gratuitous | MAJOR | CODE_SMELL | cwe, suspicious, redundant |
| pythonbugs:S3518 | Zero should not be a possible denominator | CRITICAL | BUG | cwe, denial-of-service |
| pythonbugs:S5633 | Dictionary unpacking should only be done with "mapping" objects | BLOCKER | BUG |  |
| pythonbugs:S6417 | Collections should not be modified while they are iterated | MAJOR | BUG |  |
| pythonbugs:S6464 | Non-existent dictionary keys should not be accessed | CRITICAL | BUG |  |
| pythonbugs:S6465 | Unpacking should be done with the same number of elements of the iterable. | CRITICAL | BUG |  |
| pythonbugs:S6466 | Accessing sequence elements should not trigger an IndexError | CRITICAL | BUG |  |
| pythonbugs:S6886 | offset-naive datetime.time and datetime.datetime objects should not be compared with offset-aware ones | CRITICAL | BUG |  |
| pythonbugs:S6899 | datetime.datetime objects should not be compared with datetime.date objects | CRITICAL | BUG |  |
| pythonenterprise:S7181 | PySpark Window functions should always specify a frame | CRITICAL | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7182 | The "subset" argument should be provided when using PySpark DataFrame "dropDuplicates" method | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7187 | PySpark Pandas DataFrame columns should not use a reserved name | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7189 | PySpark DataFrames used multiple times should be cached or persisted | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7191 | "withColumns" method should be preferred over "withColumn" when multiple columns are specified | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7192 | The "how" parameter should be specified when joining two PySpark DataFrames | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7193 | PySpark DataFrame toPandas function should be avoided | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7195 | PySpark lit(None) should be used when populating empty columns | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7196 | Complex logic provided to PySpark "withColumn", "filter" and "when"  methods should be refactored into separate expressions | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7468 | PySpark "dropDuplicates" subset argument should not be provided with an empty list | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7469 | PySpark's "DataFrame" column names should be unique | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7470 | PySpark's "RDD.groupByKey", when used in conjunction with "RDD.mapValues" with a commutative and associative operation, should be replaced by "RDD.reduceByKey" | MAJOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7471 | "master" and "appName" should be set when constructing PySpark "SparkContext"s and "SparkSession"s | MINOR | CODE_SMELL | pyspark, data-science |
| pythonenterprise:S7616 | Numerically stable PyTorch functions should be used instead of their unstable equivalents | BLOCKER | CODE_SMELL | machine-learning, numerical-stability, pytorch |
| pythonenterprise:S7675 | Tensor copying should use recommended methods | BLOCKER | CODE_SMELL | performance, deprecated, pytorch |
| pythonenterprise:S7693 | AI agents should be protected with guardrails | MAJOR | VULNERABILITY | cwe, former-hotspot |
| pythonenterprise:S7695 | "super()" calls should not be used in TorchScript methods | BLOCKER | BUG | torchscript, pytorch, deployment |
| pythonenterprise:S7698 | AI agent code execution should be sandboxed | MAJOR | VULNERABILITY | cwe, former-hotspot |
| pythonenterprise:S7702 | Specify "start_dim" when using "torch.flatten" to preserve batch dimension | CRITICAL | CODE_SMELL | pytorch |
| pythonenterprise:S7703 | Method calls should use parentheses when saving PyTorch model state | BLOCKER | BUG | pytorch |
| pythonenterprise:S7704 | PyTorch module classes should not be instantiated inline in forward methods | MAJOR | CODE_SMELL | machine-learning, pytorch |
| pythonenterprise:S7706 | Use PyTorch Lightning's built-in checkpointing instead of manual checkpoint saving | MAJOR | CODE_SMELL | lightning, pytorch |
| pythonenterprise:S7708 | Tensors should not be concatenated incrementally in loops | MAJOR | CODE_SMELL | machine-learning, performance, pytorch |
| pythonenterprise:S7710 | Use "torch.empty()" instead of list comprehensions for empty tensor initialization | MINOR | CODE_SMELL | readability, performance, pytorch |
| pythonenterprise:S7713 | Tensor operations should rely on automatic broadcasting instead of manual expansion | BLOCKER | CODE_SMELL | performance, pytorch |
| pythonenterprise:S8434 | Time-dependent expressions should not be used in class attributes | CRITICAL | BUG | django, timing, pitfall |
| pythonenterprise:S8435 | Sensitive data should not be passed in URL query parameters | BLOCKER | VULNERABILITY | cwe, django, owasp, privacy |
| pythonenterprise:S8437 | Class-Based Views should override "get_context_data" correctly | CRITICAL | BUG | django, framework |
| pythonenterprise:S8438 | Django view functions should declare URL parameters explicitly | CRITICAL | CODE_SMELL | django |
| pythonenterprise:S8439 | Django view functions should include all URL parameters in their signature | BLOCKER | BUG | django, url-routing |
| pythonenterprise:S8440 | Querysets should use "select_related()" or "prefetch_related()" to avoid N+1 queries | CRITICAL | CODE_SMELL | database, django, performance, orm |
| pythonenterprise:S8443 | Django Command classes should inherit from BaseCommand | BLOCKER | BUG | django, command |
| pythonenterprise:S8486 | Django middleware should call super().__init__() with appropriate parameters | BLOCKER | BUG | django, initialization, middleware |
| pythonsecurity:S2076 | OS commands should not be vulnerable to command injection attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S2078 | LDAP queries should not be vulnerable to injection attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S2083 | I/O function calls should not be vulnerable to path injection attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S2091 | XPath expressions should not be vulnerable to injection attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S2631 | Regular expressions should not be vulnerable to Denial of Service attacks | CRITICAL | VULNERABILITY | cwe, denial-of-service |
| pythonsecurity:S3649 | Database queries should not be vulnerable to injection attacks | BLOCKER | VULNERABILITY | cwe, sql |
| pythonsecurity:S5131 | Endpoints should not be vulnerable to reflected cross-site scripting (XSS) attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S5135 | Deserialization should not be vulnerable to injection attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S5144 | Server-side requests should not be vulnerable to forging attacks | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S5145 | Logging should not be vulnerable to injection attacks | MINOR | VULNERABILITY | cwe |
| pythonsecurity:S5146 | HTTP request redirections should not be open to forging attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S5147 | NoSQL operations should not be vulnerable to injection attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S5334 | Dynamic code execution should not be vulnerable to injection attacks | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S5496 | Server-side templates should not be vulnerable to injection attacks | BLOCKER | VULNERABILITY | cwe, python3 |
| pythonsecurity:S6096 | Extracting archives should not lead to zip slip vulnerabilities | BLOCKER | VULNERABILITY | cwe |
| pythonsecurity:S6287 | Applications should not create session cookies from untrusted input | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S6350 | System command arguments constructed from user input should be validated | MAJOR | VULNERABILITY | cwe, former-hotspot |
| pythonsecurity:S6547 | Environment variables should not be defined from untrusted input | MAJOR | VULNERABILITY | cwe, sans-top25-insecure |
| pythonsecurity:S6549 | Accessing files should not lead to filesystem oracle attacks | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S6639 | Memory allocations should not be vulnerable to Denial of Service attacks | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S6680 | Loop boundaries should not be vulnerable to injection attacks | CRITICAL | VULNERABILITY | cwe |
| pythonsecurity:S6776 | Stack traces should not be disclosed | MINOR | VULNERABILITY |  |
| pythonsecurity:S6839 | HTTP response headers should not be vulnerable to response splitting attacks | BLOCKER | VULNERABILITY |  |
| pythonsecurity:S7044 | Server-side requests should not be vulnerable to traversing attacks | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S7518 | Privileged prompts should not be vulnerable to injection attacks | MINOR | VULNERABILITY |  |
| pythonsecurity:S8701 | Agentic workflows should not be vulnerable to command injection attacks | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S8702 | Agentic workflows should not be vulnerable to SQL injection attacks | MAJOR | VULNERABILITY | cwe, sql |
| pythonsecurity:S8703 | Agentic workflows should not be vulnerable to server-side request forgery | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S8704 | Agentic workflows should not be vulnerable to code injection attacks | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S8705 | Agentic workflows should not be vulnerable to argument injection attacks | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S8706 | Agentic workflows should not be vulnerable to connection string injection | MAJOR | VULNERABILITY | cwe |
| pythonsecurity:S8707 | Agentic workflows should not be vulnerable to path injection attacks | MAJOR | VULNERABILITY | cwe |
