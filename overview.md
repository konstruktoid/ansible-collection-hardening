# Repository Overview: `konstruktoid.hardening`

## What is this repository?

`konstruktoid.hardening` is an Ansible **collection** — the standard packaging
format for distributing Ansible content — that applies security hardening to
systemd-based Linux servers. It targets three platform families: AlmaLinux/EL
10, Debian trixie, and Ubuntu (noble, resolute).

The collection is not a single role or playbook. It is a set of roughly 40
independent, single-purpose roles living under `roles/`, each responsible for
exactly one hardening domain: SSH configuration, sudo policy, PAM and password
quality, auditd rules, kernel and network sysctl settings, firewalling
(UFW), filesystem mount options, kernel module blocklisting, systemd-journald
and logind configuration, package management policy, and more. A consumer
installs the collection and then applies whichever roles are relevant to
their fleet — there is no umbrella role that must be taken all-or-nothing.

The project is a collection-format conversion of an earlier, older project,
[`ansible-role-hardening`](https://github.com/konstruktoid/ansible-role-hardening),
which packaged the same hardening logic as one monolithic Ansible role. This
repository re-architects that logic into discrete roles so users can adopt
individual controls, test them independently, and reason about their
`meta/main.yml` platform support and `defaults/main.yml` variables in
isolation.

It is maintained by Thomas Sjögren (`@konstruktoid`) and licensed under
Apache-2.0.

## Why does it exist?

Hardening a Linux server by hand against a benchmark like CIS or DISA STIG is
tedious, error-prone, and hard to keep consistent across a fleet or repeat
after a rebuild. This collection exists to make that hardening:

- **Automatable** — every control is expressed as idempotent Ansible tasks
  that can be run against one host or thousands, repeatedly, without drift.
- **Composable** — because each hardening domain is its own role instead of
  one large role, an operator can apply exactly the subset of controls that
  fits their environment (for example, using `ssh` and `sudo` hardening
  without touching firewall or kernel module policy), rather than accepting
  an opinionated bundle wholesale.
- **Auditable and reviewable** — each role's tasks map to concrete file
  edits (`sshd_config`, `sysctl.d`, `login.defs`, PAM stacks, auditd rules,
  etc.), so a reviewer can see precisely what system state a given role
  enforces, and CI (`ansible-lint`, `molecule`) verifies that state on real
  target platforms.
- **A migration path** — for existing users of `ansible-role-hardening`,
  it offers equivalent (or more granular) coverage in the more modern,
  Galaxy-distributable collection format, without them having to hand-roll
  the split themselves.

## What security philosophy does it follow?

The philosophy is documented explicitly in `.github/copilot-instructions.md`
and echoed in `CLAUDE.md`, and it shapes both the shipped roles and how
contributions are reviewed:

- **Standards-aligned, not standards-invented.** Recommendations and default
  settings are biased toward CIS Benchmarks, DISA STIG guidance, and
  CMMC-oriented practices, rather than one-off opinions about "good"
  security.
- **Secure by default, least privilege, least functionality.** Roles default
  to restrictive file permissions and ownership, minimal `become` scope,
  reduced attack surface, and explicit rather than implicit configuration.
  Nothing is silently permissive.
- **Preserve hardening intent.** Existing controls should not be weakened or
  relaxed without an explicit, deliberate request — and any such change must
  document the security rationale and compatibility tradeoff. High-sensitivity
  domains (SSH, sudo, PAM, audit/logging, SELinux/AppArmor, firewalling,
  mounts, sysctl, services, authentication) get extra scrutiny.
- **Auditability over cleverness.** Module-first authoring (always fully
  qualified collection names, no bare module names), declarative and
  idempotent tasks, explicit conditions, and avoidance of `shell`/`command`
  where a real module exists. Clever one-liners and non-idempotent shell
  hacks are discouraged because they're harder to audit and reason about.
  Broad network exposure, permissive firewall rules, and world-writable
  modes are treated as defects, not conveniences.
- **No hardcoded secrets, anywhere** — in tasks, defaults, or templates.
- **Verify, don't assert.** The philosophy isn't just "write secure-looking
  YAML" — every role is expected to be converged and verified against real
  target images (via `molecule`) so that claimed hardening behavior is
  checked on-machine, not just asserted in code.

## What are its major components?

- **`roles/`** — the actual content: ~40 roles, one per hardening domain
  (e.g. `ssh`, `sudo`, `password_management`, `auditd`, `sysctl`, `kernel`,
  `kernel_modules`, `mount`, `ufw`, `journald`, `usbguard`, `apparmor`,
  `package_management`, `login_defs`, `umask`, and others). Each follows the
  standard Ansible role layout (`defaults/`, `meta/`, `tasks/`), uses
  role-prefixed variable names (e.g. `umask_value`, `rsyslog_filecreatemode`),
  and declares its own supported platforms in `meta/main.yml`. Most roles
  edit system configuration files directly (`lineinfile`, `replace`, `copy`)
  rather than rendering Jinja templates.
- **`extensions/molecule/`** — the shared test harness for all roles, with
  three interchangeable provisioning scenarios (`docker`, `default` via
  direct `qemu-system-x86_64` boot of genericcloud images, and `vagrant` via
  VirtualBox) that all converge and verify the exact same role set through
  common `resources/converge.yml` and `resources/verify.yml` /
  `tests/verify_<role>.yml` files.
- **`galaxy.yml` / `meta/runtime.yml`** — collection metadata (namespace
  `konstruktoid`, name `hardening`), the `ansible-core` version floor
  (>=2.18.0), and declared collection dependencies (`ansible.posix`,
  `community.crypto`, `community.general`).
- **CI and review policy** — `.ansible-lint` (production profile, no
  suppression of new findings), `tox.ini` environments (`docker`, `devel`,
  `upstream`) that chain linting and molecule testing, and
  `.github/copilot-instructions.md` / `.github/instructions/*` as the
  authoritative rulebook for both human and AI-assisted contributions,
  including a dedicated `github-actions.instructions.md` for workflow/action
  changes (least-privilege permissions, SHA-pinned third-party actions, no
  curl-pipe-to-shell).
- **Per-role documentation** — each role ships its own `README.md`
  describing its variables and example usage, referenced from the top-level
  `README.md`'s role table; there is no single combined "run everything"
  playbook to document instead.

## What does it not try to do?

- **It is not a single opinionated "hardened server" playbook.** There is
  intentionally no top-level playbook or umbrella role that applies every
  control at once with one command; composing a subset (or all) of the
  roles is left to the consumer.
- **It does not invent novel security controls.** It implements and
  automates existing, recognized guidance (CIS/STIG/CMMC-aligned), not
  bespoke hardening ideas.
- **It does not guarantee compliance certification.** Applying the roles
  moves a host toward benchmark alignment; it does not, by itself,
  constitute a compliance audit, attestation, or certification.
  `SECURITY.md` only commits to supporting the current upstream and latest
  published release, with issues/PRs as the reporting channel — there is no
  dedicated security team or formal SLA.
- **It does not cover every OS or every hardening domain universally.**
  Platform coverage is declared per role (some roles, like `apparmor`,
  `apport`, `ufw`, and `motd_news`, are Debian/Ubuntu-only and have no
  AlmaLinux/EL equivalent), and the collection is scoped to systemd-based
  Linux — it does not address non-systemd distributions, other operating
  systems, containers/Kubernetes hardening, or cloud-provider-specific
  controls.
- **It does not manage secrets or credentials.** Consistent with its "never
  hardcode secrets" rule, it has no built-in secrets-management, vaulting,
  or credential-rotation functionality — that's left to the consumer's own
  tooling (e.g. Ansible Vault, external secret stores).
- **It does not prioritize convenience over auditability.** Shell one-liners,
  implicit fallbacks, and permissive defaults that might make setup "easier"
  are explicitly discouraged even where they would reduce the amount of
  YAML — the project trades some ergonomics for reviewability and
  idempotence.
