---
source: https://docs.djangoproject.com/en/stable/topics/security/
doc_type: framework_doc
framework: django
topic: xss
accessed_at: 2026-09-09
---

# Django Security - Cross Site Scripting

Cross-Site Scripting occurs when untrusted content is rendered as executable
HTML or JavaScript in a user's browser.

Django templates escape HTML output by default.

## Risky patterns

XSS risks can appear when automatic escaping is disabled or when untrusted data
is marked as safe.

## Recommended mitigation

Keep automatic template escaping enabled.

Avoid marking user-controlled content as safe unless it has been properly
validated or sanitized.