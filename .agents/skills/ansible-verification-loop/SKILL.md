---
name: ansible-verification-loop
description: Implements and verifies changes to Ansible roles, playbooks, and tasks in this hardening collection through a bounded lint-test-fix loop. Use when reviewing or modifying anything under roles/, playbooks, or other Ansible collection content in this repository.
---

# ansible-verification-loop

## When to use
- Reviewing or modifying Ansible roles, playbooks, or tasks in this collection.

## When not to use
- Changes that don't touch Ansible collection content.

## Workflow

Copy this checklist into your response and check off items as you complete them:

```
Ansible change progress:
- [ ] Step 1: Read the role's defaults/main.yml, tasks/main.yml, meta/main.yml (+ galaxy.yml/meta/runtime.yml if relevant)
- [ ] Step 2: Apply the change, following repo conventions and security rules
- [ ] Step 3: Sync galaxy_info.platforms and docs/argspec if OS logic or defaults changed
- [ ] Step 4: Update verify_<role>.yml / converge.yml if role behavior or variables changed
- [ ] Step 5: Run the verification loop until clean or 3 attempts are exhausted
- [ ] Step 6: Report the result, including any unresolved issues
```

**Step 1: Read before changing.** Read the role's `defaults/main.yml`, `tasks/main.yml`, and
`meta/main.yml`, plus any dependencies (`galaxy.yml`, `meta/runtime.yml`) or requirements.

**Step 2: Apply the change.** Follow `.github/copilot-instructions.md` and
`.github/instructions/*.instructions.md` — the authoritative security/quality rules for this repo
(FQCN only, double-quoted strings, quoted octal `mode` with explicit `owner`/`group`,
role-prefixed variable names, treat SSH/sudo/PAM/audit/SELinux/AppArmor/firewall/mounts/sysctl/
services/auth as high-sensitivity). Follow existing naming, file structure, and style conventions.

When writing or editing YAML, follow the [YAML 1.2.2 spec](https://yaml.org/spec/1.2.2/). Ansible's
loader is YAML-1.1-flavored (bare `yes`/`no`/`on`/`off` parse as booleans, which YAML 1.2's core
schema would treat as plain strings), so always use explicit `true`/`false` and quote any scalar
that could be misread as a different type across the two specs (leading-zero numbers,
sexagesimal-looking `NN:NN` strings, etc). Do not use tabs for indentation.

**Step 3: Sync dependents.** If OS-conditional logic changed, keep `roles/<name>/meta/main.yml`
`galaxy_info.platforms` in sync with it. If default values or argument specs changed, update all
relevant documentation (README, role docs, defaults/argspec, etc).

**Step 4: Update test coverage.** This repo has no per-role test setup — all roles are exercised
together via `extensions/molecule/resources/converge.yml` and verified via
`extensions/molecule/tests/verify_<role>.yml`, included from `resources/verify.yml`. When adding or
changing a role, add/update its `verify_<role>.yml` and, if it needs scenario-specific variables,
its `vars:` block in `converge.yml`.

## Step 5: Verification loop (run validator → fix → repeat)

1. Run `ansible-lint` and confirm a clean result. This is the primary quality gate — do not add
   suppressions to `.ansible-lint-ignore` to silence findings from new changes. Do not proceed
   until it passes.
2. Run `tox -e docker` and confirm exit code 0. This installs role dependencies
   (`requirements.yml`), re-runs `ansible-lint`, then invokes `molecule test -s docker` to converge
   and verify all roles in containers (almalinux10, ubuntu resolute, debian trixie), including an
   idempotence check.
   - While iterating on a single role, use `molecule converge -s docker` / `molecule verify -s
     docker` instead of the full cycle to save time — but always finish with a full `tox -e docker`
     (or `molecule test -s docker`, after installing `requirements.yml` and running `ansible-lint`
     yourself) before treating the change as verified.
3. If step 2 fails: fix the issue and return to step 1. This counts as one attempt. One **attempt**
   is one full fix-and-rerun cycle: apply fixes for the findings from the previous run, then rerun
   the verification commands to completion. Reading output or re-reading a file without changing
   anything is not an attempt.
4. Repeat until every check passes, bounded as follows:
   - Baseline the loop at 3 attempts.
   - Continue past 3 only while making measurable progress, meaning each cycle ends with strictly
     fewer findings than the one before it.
   - Stop early, before 3 attempts, if the loop is oscillating: the same findings recur, the count
     stops dropping, or a fix for one finding reintroduces another.
   - When stopping for either reason, report to the user rather than proceeding or silently giving
     up. Name the failing check, include its output, and state what was tried.

## Reporting and redaction

Report any issues found during verification, with detailed reproduction steps and relevant
logs/output. Ansible output is unusually rich in machine detail: play recaps and `--diff` output
name the target host, gathered facts carry hostnames, interfaces and internal addresses, and
failure messages quote absolute paths under the invoking user's home. Strip that before pasting
output anywhere it will be stored, and never commit it into the repository. The same applies to
anything checked in as a fixture: use `localhost`, `example.com`, or RFC 5737 addresses
(`192.0.2.0/24`) in inventories, host vars, and templates rather than a real host.

## Step 6: Final checklist

Never declare this done from the edit alone. Confirm each of the following before reporting
success:
- [ ] `ansible-lint` passes
- [ ] `tox -e docker` / `molecule test -s docker` passes
- [ ] Idempotence holds (no changes reported on molecule's second converge)
- [ ] `verify_<role>.yml` and `converge.yml` updated if a role's behavior or variables changed
- [ ] `meta/main.yml` `galaxy_info.platforms` still matches any OS-conditional logic
- [ ] No user or system information committed: inventories, host vars, templates, and any captured
      lint or molecule output use placeholder hosts and addresses, with no real hostname, home
      directory path, username, or internal IP
- [ ] No unrelated files changed
- [ ] New/changed YAML has no YAML-1.1/1.2 ambiguities (bare `yes`/`no`/`on`/`off`, unquoted
      leading-zero numbers, sexagesimal-looking strings, tab indentation) — `ansible-lint`'s
      `yaml[truthy]` rule catches the boolean case, but review the rest by eye

## References

- [references/yaml-quoting.md](references/yaml-quoting.md): YAML 1.2.2 scalar resolution and
  quoting, including the "Norway problem". Read it when a change touches quoting in a YAML file,
  or when justifying why a value must stay quoted.
