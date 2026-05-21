---
applyTo: "**/*.yml,**/*.yaml,**/roles/**/*.yml,**/roles/**/*.yaml,**/tasks/**/*.yml,**/tasks/**/*.yaml,**/handlers/**/*.yml,**/handlers/**/*.yaml,**/defaults/**/*.yml,**/defaults/**/*.yaml,**/vars/**/*.yml,**/vars/**/*.yaml,**/meta/**/*.yml,**/meta/**/*.yaml,**/playbooks/**/*.yml,**/playbooks/**/*.yaml,**/*.j2,**/templates/**/*.j2"
---

# Enterprise Ansible Hardening Instructions

Apply these rules to Ansible YAML and Jinja changes.

## Authoring priorities
- Module-first implementation; avoid `shell`/`command` unless no safe module exists.
- Declarative, idempotent tasks with descriptive names.
- Explicit `owner`, `group`, and restrictive quoted octal `mode` for managed files.
- Restrictive defaults in vars/defaults/templates.
- Handlers for config-driven restart/reload behavior.

## Conservative security handling
Treat these domains as high sensitivity and change conservatively:
- SSH, sudo, PAM, authentication, and user/group management
- audit/logging and systemd service behavior
- mounts, sysctl/kernel tuning, SELinux, firewall rules
- crypto policy, protocol hardening, and service exposure

## Compliance-aware behavior
- Favor patterns aligned with CIS and STIG hardening intent and CMMC-oriented objectives.
- Improve auditability, traceability, and enforcement consistency.
- Mention likely control areas only when justified; do not invent exact control IDs.

## Review priorities
1. Security regression or weakening of existing hardening intent
2. Over-privileged execution (`become`, root scope, broad permissions)
3. Non-idempotent logic or risky shell pipelines
4. Missing explicit ownership/mode on sensitive files
5. Operational reliability issues (unsafe restarts, brittle conditions)

## Risk levels
- Critical: clear security bypass, credential exposure, or severe privilege expansion
- High: significant hardening regression or broad exposure
- Medium: moderate hardening gap or reliability risk
- Low: maintainability/readability issue with minimal security impact
