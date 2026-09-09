---
source: https://docs.djangoproject.com/en/stable/topics/security/
doc_type: framework_doc
framework: django
topic: csrf
accessed_at: 2026-09-09
---

# Django Security - Cross Site Request Forgery

Cross-Site Request Forgery occurs when an attacker causes an authenticated user
to submit an unwanted request to an application.

Django provides built-in CSRF protection for unsafe HTTP methods.

## Recommended mitigation

Use Django's CSRF middleware and include CSRF tokens in forms that perform
state-changing actions.

Do not disable CSRF protection unless there is a specific and justified reason.