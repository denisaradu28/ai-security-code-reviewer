---
source: https://docs.djangoproject.com/en/stable/topics/security/
doc_type: framework_doc
framework: django
topic: sql_injection
accessed_at: 2026-09-09
---

# Django Security - SQL Injection

Django querysets are protected from SQL injection when queries are constructed
using the ORM normally.

Risks appear when raw SQL is used incorrectly or when user-controlled data is
inserted directly into SQL strings.

## Risky pattern

Building SQL commands through string concatenation or formatting with external
input can allow attackers to alter the intended query.

## Recommended mitigation

Prefer the Django ORM whenever possible.

When raw SQL is required, use parameterized queries and pass parameters
separately rather than embedding user-controlled values directly into the SQL
statement.