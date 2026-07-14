# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

`konstruktoid.hardening` is an Ansible collection that hardens systemd-based Linux hosts
(AlmaLinux/EL, Debian, Ubuntu), converted from
[ansible-role-hardening](https://github.com/konstruktoid/ansible-role-hardening). It is a
collection of ~40 independent roles under `roles/`, each responsible for one hardening domain
(SSH, sudo, PAM, auditd, sysctl, firewall, mounts, kernel modules, etc.), rather than a single
monolithic role.

## Commands

Test/lint dependencies: `pip install -r requirements.txt` (pins `ansible-core`, `ansible-lint`,
`molecule`). `upstream-requirements.txt` is the unpinned variant used by the `upstream`/
`docker-upstream` tox environments.

- `ansible-lint` — lint against `profile: production` (`.ansible-lint`). This is the primary
  quality gate; do not add suppressions to `.ansible-lint-ignore` to silence findings from new
  changes.
- `tox -e docker` — full test loop: installs role dependencies (`requirements.yml`), runs
  `ansible-lint`, then `molecule test -s docker`.
- `molecule test -s docker` (run from repo root, or `cd extensions/molecule/docker`) — creates
  containers for almalinux10, ubuntu (resolute), and debian (trixie), converges all roles, checks
  idempotence, then runs verifiers.
- `molecule converge -s docker` / `molecule verify -s docker` — iterate on a single stage instead
  of the full destroy/create/idempotence/verify sequence.
- `tox -e devel` / `tox -e upstream` — same loop against the `default` scenario, or against
  unpinned upstream `ansible-core`/`ansible-lint`.
- `molecule test` (from `extensions/molecule/default`, or `molecule test -s default` from the
  repo root) — the `default` scenario. It boots AlmaLinux 10, Ubuntu resolute, and Debian trixie
  genericcloud images directly with `qemu-system-x86_64` (UEFI/OVMF, cloud-init NoCloud seed ISOs
  built with `genisoimage`), instead of containers. Requires `qemu-system-x86_64`, `qemu-img`,
  `genisoimage`, and OVMF firmware (`/usr/share/OVMF/OVMF_{CODE,VARS}_4M.fd`) on the host; base
  images are cached under `~/.cache/molecule-qemu/images`.
- `molecule test -s vagrant` — same suite against VirtualBox VMs via Vagrant
  (`extensions/molecule/vagrant`); requires `vagrant` and VirtualBox installed locally.
- `tox -e os-devel` / `molecule test -s os-devel` (`extensions/molecule/os-devel`, qemu-booted like
  the `default` scenario) — tests against upcoming/development OS releases: Debian 14 "forky" and
  Ubuntu 26.10 "stonking", using their daily/current cloud images. Kept separate from the stable
  `docker`/`default`/`vagrant` scenarios since these releases are still moving targets, and is
  local-development-only (no CI workflow) since it needs the same qemu/OVMF host setup as
  `default`.

There is no per-role test setup: all roles are exercised together via
`extensions/molecule/resources/converge.yml`, and verified via
`extensions/molecule/tests/verify_<role>.yml` files included from
`extensions/molecule/resources/verify.yml`. When adding or changing a role, add/update its
`verify_<role>.yml` and, if it needs scenario-specific variables, its `vars:` block in
`converge.yml`.

## Architecture

- `roles/<name>/{defaults,meta,tasks}/main.yml` — standard Ansible role layout. Most roles have
  no `handlers/`, `templates/`, or `vars/`; config is applied via `lineinfile`/`replace`/`copy`
  etc. directly against system files, not templates.
- `roles/<name>/meta/main.yml` declares `galaxy_info.platforms` per role — keep this in sync with
  any OS-conditional logic added to that role's tasks.
- `extensions/molecule/` holds the single molecule setup shared by all roles, with three
  scenarios that differ only in how instances are provisioned (all three converge/verify the
  same roles via `resources/`):
  - `default/` and `os-devel/` — both use `driver: name: default` and point their
    `provisioner.playbooks.create`/`destroy` at the shared `resources/create_qemu.yml` and
    `resources/destroy_qemu.yml`, which boot genericcloud qcow2 images directly via
    `qemu-system-x86_64` and register them into a dynamic molecule inventory. Only their
    `molecule.yml` platform matrices differ (stable vs. devel images).
  - `docker/` — `molecule.yml` platform matrix of containers, plus its own `create.yml`/
    `destroy.yml` using `community.docker.docker_container`.
  - `vagrant/` — Vagrant/VirtualBox VMs, with `Vagrantfile.j2` rendered per-run from the
    platform matrix and its own `create.yml`/`destroy.yml` driving `vagrant up`/`vagrant destroy`.
  - `resources/converge.yml` — applies every role to the test hosts in a fixed order, with
    scenario-only variable overrides (e.g. `sshd_allow_groups`, `ufw_admin_net`).
  - `resources/prepare.yml` / `resources/verify.yml` — pre-test setup and the entrypoint that
    includes per-role `tests/verify_<role>.yml` files.
  - `resources/create_qemu.yml` / `resources/destroy_qemu.yml` — shared QEMU provisioning logic
    for the `default` and `os-devel` scenarios (see above).
- `meta/runtime.yml` sets `requires_ansible`; `galaxy.yml` declares collection metadata,
  dependencies (`ansible.posix`, `community.crypto`, `community.general`), and `build_ignore`.
- `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md` are the
  authoritative security/quality rules for this repo — follow them for any change here too:
  - Module-first, always FQCN (`ansible.builtin.*`, `ansible.posix.*`, …), never bare module names.
  - Double-quoted YAML strings; quoted octal `mode` strings (e.g. `mode: "0640"`) with explicit
    `owner`/`group` on managed files.
  - Role-scoped variable names prefixed with the role name (e.g. `umask_value`,
    `rsyslog_filecreatemode`) in `defaults/main.yml`.
  - Treat SSH, sudo, PAM, audit/logging, SELinux/AppArmor, firewalling, mounts, sysctl, services,
    and authentication as high-sensitivity: preserve existing hardening intent, don't silently
    weaken or broaden access, and document security rationale/compatibility tradeoffs for
    sensitive changes.
  - `.github/instructions/github-actions.instructions.md` applies if you add/edit files under
    `.github/workflows/` or `action.yml` (least-privilege `permissions`, pinned third-party
    actions by SHA, no curl-pipe-to-shell, explicit `timeout-minutes`/`concurrency`).
