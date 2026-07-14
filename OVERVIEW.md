# Repository Overview: `konstruktoid.hardening`

## Introduction

`konstruktoid.hardening` is an Ansible collection, the standard packaging
format for distributing Ansible content, that applies security hardening to
systemd-based Linux servers. It targets three platform families: AlmaLinux
and other Enterprise Linux (EL) derivatives at version 10, Debian trixie, and
Ubuntu (noble, resolute).

The collection is not a single role or playbook. It consists of
approximately 40 independent, single-purpose roles under `roles/`, each
responsible for one hardening domain: SSH configuration, sudo policy, PAM
and password quality, auditd rules, kernel and network sysctl settings,
firewalling (UFW), filesystem mount options, kernel module blocklisting,
systemd-journald and logind configuration, package management policy, and
others. A consumer installs the collection and applies whichever roles are
relevant to their fleet; there is no umbrella role that must be applied in
full.

The intended audience is system administrators, platform engineers, and
security teams who manage systemd-based Linux hosts with Ansible and need
repeatable, auditable hardening controls aligned to recognized benchmarks.

## Purpose

Hardening a Linux server by hand against a benchmark such as CIS or DISA STIG
is tedious, error-prone, and difficult to keep consistent across a fleet or
repeat after a rebuild. This collection exists to make that hardening
automatable, composable, and auditable.

For existing users of `ansible-role-hardening`, the collection also offers a
migration path: equivalent or more granular coverage in the Galaxy
distributable collection format, without requiring users to perform the
role split themselves.

## Major Components

**Roles** form the substantive content of the collection: approximately 40
roles, one per hardening domain, such as `ssh`, `sudo`,
`password_management`, `auditd`, `sysctl`, `kernel`, `kernel_modules`,
`mount`, `ufw`, `journald`, `usbguard`, `apparmor`, `package_management`,
`login_defs`, and `umask`, among others. Each role follows the standard
Ansible role layout, uses role-prefixed variable names, and declares its own
supported platforms independently. Most roles edit system configuration
files directly rather than rendering templates, which keeps the relationship
between a task and the resulting file change direct and auditable.

The **test harness** is a shared framework used by every role rather than a
per-role testing setup. It provides interchangeable provisioning scenarios,
using containers or directly booted virtual machine images, that all
converge and verify the same set of roles through common configuration and
verification files. This shared approach ensures that all roles are
exercised together under realistic, consistent conditions rather than in
isolation.

**Collection metadata** declares the collection's namespace and name, the
minimum supported `ansible-core` version, and its dependencies on other
Ansible collections required by specific roles. This metadata governs how
the collection is published, installed, and resolved alongside its
dependencies.

**CI and review policy** ties the roles and test harness together through
linting configuration, environment definitions that chain linting and
testing, and a documented rulebook for both human and AI-assisted
contributions. This policy is what keeps roles conforming to the project's
security philosophy over time, rather than relying on ad hoc review.

**Per-role documentation** accompanies each role, describing its variables
and example usage, and is referenced from the top-level `README.md`'s role
table. There is no single combined "run everything" playbook to document in
its place.

## Scope

The collection is intended to provide security hardening controls for
systemd-based Linux servers running AlmaLinux or other EL derivatives,
Debian, or Ubuntu. Its included functionality covers operating system and
service-level hardening domains: authentication and access control, kernel
and network parameters, filesystem and mount protections, logging and
auditing, firewalling, and package and update management.

Intended use cases include applying individual roles selectively to fit an
organization's existing configuration, applying the full set of roles to
establish a comprehensive baseline, and using the collection as a reference
implementation of CIS- and STIG-aligned controls for systemd-based Linux.
Each role is expected to be idempotent, independently testable, and safe to
re-run against already-hardened hosts without unintended side effects.

## Out of Scope

It does not invent novel security controls. It implements and automates
existing, recognized guidance rather than bespoke hardening ideas.

It does not guarantee compliance certification. Applying the roles moves a
host toward benchmark alignment, but does not by itself constitute a
compliance audit, attestation, or certification.

It does not cover every operating system or every hardening domain
universally. Platform coverage is declared per role; some roles, such as
`apparmor`, `apport`, `ufw`, and `motd_news`, are specific to Debian and
Ubuntu and have no AlmaLinux or EL equivalent. The collection is scoped to
systemd-based Linux and does not address non-systemd distributions, other
operating systems, container or Kubernetes hardening, or cloud-provider-
specific controls.

It does not manage secrets or credentials. Consistent with its rule against
hardcoded secrets, it has no built-in secrets management, vaulting, or
credential rotation functionality; that responsibility is left to the
consumer's own tooling.

It does not prioritize convenience over auditability. Shell one-liners,
implicit fallbacks, and permissive defaults that might simplify setup are
discouraged even where they would reduce the amount of configuration
required, because the project trades some ergonomics for reviewability and
idempotence.

## Architecture Summary

The collection has no central controller or orchestration layer. Each role
under `roles/` is a self-contained unit that reads its own default
variables, checks the current platform against its declared support, and
applies its tasks directly to system configuration files. Roles do not call
one another, and there is no shared state passed between them beyond the
conventions established by the standard Ansible role layout.
