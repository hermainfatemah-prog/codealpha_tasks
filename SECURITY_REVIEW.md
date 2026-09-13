# CodeAlpha Cyber Security Internship — Task 3
## Secure Coding Review

### 1. Application and language selected
- **Language:** Python
- **Application:** Small Flask-based demo login/user API
- **Review method:** Manual source-code inspection with security-focused checks.
- **Purpose:** Identify security weaknesses in authentication, database access, configuration, and data exposure, then document remediation.

### 2. Scope
The reviewed application contains three relevant areas:
1. User lookup through SQLite.
2. A login endpoint.
3. A user-information endpoint.

The file `vulnerable_app.py` is intentionally insecure for demonstration and review. `secure_app.py` shows the corresponding remediated patterns.

### 3. Findings

| ID | Severity | Finding | Evidence | Recommended remediation |
|---|---|---|---|---|
| SC-01 | High | SQL injection risk | User input is concatenated into the SQL statement in `get_user()` | Use parameterized/prepared queries and never concatenate untrusted input into SQL |
| SC-02 | High | Hard-coded plaintext demo credentials | Login compares input against a fixed username/password in source code | Remove hard-coded credentials; store password hashes and use a secret/credential management system |
| SC-03 | Medium | No brute-force protection | `/login` has no rate limiting or lockout control | Add rate limiting, progressive delays, monitoring, and appropriate account lockout controls |
| SC-04 | Medium | Excessive data exposure risk | `/user` returns database-derived fields directly | Return only required fields and apply authorization checks |
| SC-05 | Medium | Debug mode enabled | `app.run(debug=True)` in the vulnerable version | Disable debug mode in production and configure errors/logging safely |

### 4. Remediation implemented
The `secure_app.py` example demonstrates:
- Parameterized SQLite queries using `?` placeholders.
- Password verification with `werkzeug.security.check_password_hash`.
- Database path supplied through an environment variable.
- Debug mode disabled.
- Reduced response data.
- Comments identifying where production rate limiting and generic authentication responses should be added.

### 5. Secure coding best practices
- Validate and constrain untrusted input.
- Use parameterized database queries.
- Never hard-code passwords, API keys, or tokens.
- Store passwords using strong salted password hashing.
- Apply least privilege and authorization checks.
- Return only necessary data from APIs.
- Disable debug/development settings in production.
- Add rate limiting to authentication endpoints.
- Keep dependencies updated and review security advisories.
- Log security-relevant events without storing passwords or sensitive secrets.
- Run automated static analysis and dependency/security checks as part of development.

### 6. Verification checklist
- [x] Programming language and application selected.
- [x] Security-focused code review performed.
- [x] Vulnerabilities documented with severity and evidence.
- [x] Remediation steps provided.
- [x] Safer code example included.
- [x] Secure coding recommendations documented.

### 7. Conclusion
The review identified database injection risk, insecure credential handling, missing brute-force protection, potential excessive data exposure, and unsafe debug configuration. The remediated example demonstrates safer database access, password verification, configuration handling, and reduced data exposure.

**Note:** This is a controlled educational demo created for the internship task. It is not intended for production deployment without further testing, authentication design, authorization controls, logging, rate limiting, dependency management, and security testing.
