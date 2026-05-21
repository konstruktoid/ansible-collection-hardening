# Repository Instructions for GitHub Copilot

This repository is an Ansible collection for Linux security hardening. Prefer secure-by-default, operationally reliable, maintainable, and auditable changes.

## Mission and baseline
- Preserve existing hardening intent unless an explicit deviation is requested.
- Bias recommendations toward CIS Benchmarks, DISA STIG guidance, and CMMC-oriented practices.
- Prefer minimal, reviewable, reversible diffs.

## Engineering expectations
- Use declarative, idempotent Ansible solutions.
- Prefer built-in and well-supported modules over ad hoc shell/command usage.
- Use clear task names, explicit conditions, and deterministic behavior.
- Favor maintainability over clever one-liners.

## Security requirements
- Enforce least privilege; do not broaden `become` scope without need.
- Use restrictive ownership and permissions by default.
- Never hardcode secrets, credentials, keys, tokens, or passwords.
- Treat SSH, sudo, PAM, audit/logging, SELinux, firewalling, mounts, sysctl, services, and authentication settings as high-sensitivity areas.
- Avoid security relaxations unless explicitly requested and documented.

## Preferred patterns
- Module-first authoring (`ansible.builtin.*`, `ansible.posix.*`, and purpose-built modules).
- Explicit `owner`, `group`, and quoted octal string `mode` values (for example `mode: "0640"`) for managed files.
- Handlers for restart/reload on config changes.
- Safe defaults in vars/templates and explicit tradeoff notes when compatibility requires softer settings.

## Discouraged patterns
- `shell`/`command` when an Ansible module exists.
- Non-idempotent logic without proper guards.
- Broad network exposure, permissive firewall rules, or world-writable modes.
- Implicit behavior that reduces auditability.

## Linux security posture guidance
- Prefer restrictive defaults, reduced attack surface, and least functionality.
- Keep access control, logging/auditing, and configuration enforcement explicit.
- Do not weaken hardening controls silently.

## Template and Jinja guidance
- Keep templates deterministic and explicit.
- Do not embed secrets in templates.
- Avoid permissive fallback values unless explicitly required.

## Documentation guidance
- Explain security rationale and operational impact for sensitive changes.
- Note compatibility tradeoffs and any intentional deviation from hardening intent.

## Review expectations
Prioritize findings on:
- security misconfiguration,
- privilege escalation,
- file ownership/mode,
- idempotency,
- unsafe module choice,
- exposure in network/service/authentication paths.

For meaningful findings, provide: Finding, Risk (Critical/High/Medium/Low), Location, Recommendation, and safer example as a short code snippet.

## Change safety rules
- Do not remove or weaken hardening behavior without explicit instruction.
- Do not silently broaden access or reduce enforcement.
- Flag high-impact changes affecting remote access, boot behavior, authentication, or audit posture.
