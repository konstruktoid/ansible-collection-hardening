---
name: ansible-verification-loop
description: Use this skill when reviewing or modifying Ansible collections, playbooks, roles, or tasks.
---

# ansible-verification-loop

## Purpose
Provide a structured approach for reviewing and modifying Ansible collections, playbooks, roles, or
tasks in this repository. It ensures changes are made consistently, verified thoroughly, and
documented clearly.

## When to use this
- When reviewing or modifying Ansible collections, playbooks, roles, or tasks.
- When you need to ensure that changes are made consistently and verified thoroughly.

## When NOT to use this
- When making changes that do not involve Ansible collections, playbooks, roles, or tasks.

## Steps
1. Read the relevant role's `defaults/main.yml`, `tasks/main.yml`, and `meta/main.yml` before making
   any changes, plus any dependencies (`galaxy.yml`, `meta/runtime.yml`) or requirements.
2. Follow `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md` — the
   authoritative security/quality rules for this repo (FQCN only, double-quoted strings, quoted
   octal `mode` with explicit `owner`/`group`, role-prefixed variable names, treat SSH/sudo/PAM/
   audit/SELinux/AppArmor/firewall/mounts/sysctl/services/auth as high-sensitivity).
3. Follow the existing conventions and patterns in the codebase: naming, file structure, and style.
4. If OS-conditional logic changes, keep `roles/<name>/meta/main.yml` `galaxy_info.platforms` in
   sync with it.
5. If default values or argument specs change, update all relevant documentation (README, role
   docs, defaults/argspec, etc).
6. Add or update test coverage for the change:
   - This repo has no per-role test setup — all roles are exercised together via
     `extensions/molecule/resources/converge.yml` and verified via
     `extensions/molecule/tests/verify_<role>.yml`, included from `resources/verify.yml`.
   - When adding or changing a role, add/update its `verify_<role>.yml` and, if it needs
     scenario-specific variables, its `vars:` block in `converge.yml`.
7. Verify the change (see checklist below). If any issues are found, fix them and re-verify. Repeat
   until all issues are resolved or verification has been attempted 3 times, whichever comes first.
   If issues remain unresolved after 3 attempts, stop and report to the user instead of proceeding
   or silently giving up.
8. Report any issues found during verification, with detailed reproduction steps and relevant
   logs/output.

## Verify
- Run `ansible-lint` and confirm a clean exit / expected output. This is the primary quality gate —
  do not add suppressions to `.ansible-lint-ignore` to silence findings from new changes.
- Run `tox -e docker` and confirm exit code 0. This installs role dependencies
  (`requirements.yml`), runs `ansible-lint`, then invokes `molecule test -s docker` to converge and
  verify all roles in containers (almalinux10, ubuntu resolute, debian trixie), including an
  idempotence check.
- Running `molecule test -s docker` directly (from repo root, or `cd extensions/molecule/docker`)
  skips the dependency install and lint steps that `tox -e docker` performs first — install
  `requirements.yml` and run `ansible-lint` yourself beforehand if you use this form instead of
  `tox`.
- While iterating on a single role, use `molecule converge -s docker` / `molecule verify -s docker`
  instead of the full `test` cycle to save time, but always finish with a full `molecule test -s
  docker` (or `tox -e docker`) before declaring the change verified.

## Verification checklist
Never declare this done based on the edit alone. Confirm each of the following:
- [ ] Lint passes: `ansible-lint`
- [ ] Tests pass: `tox -e docker` / `molecule test -s docker`
- [ ] Idempotence holds (no changes reported on molecule's second converge)
- [ ] `verify_<role>.yml` and `converge.yml` updated if a role's behavior or variables changed
- [ ] `meta/main.yml` `galaxy_info.platforms` still matches any OS-conditional logic
- [ ] No unrelated files changed
