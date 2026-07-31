# Change Log

## Unreleased

- Add `file_permissions` role, restricting the ownership and permissions of the account
  databases (`/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/gshadow`, their backup files
  and `/etc/security/opasswd`) and of the bootloader configuration files.

## 0.2.0 (2026-07-23)

- Add `firewalld` role.
- Add `llmr` and multicast sysctl options.
- Update collection support documentation to reflect what is actually supported.
- Harden GitHub Actions workflows (SLSA, least-privilege permissions, `author_association` gate).
- Add and update Claude Code verification loop tooling under `.claude/`.
- Remove Vagrant, dedup and improve testing.

## 0.1.1 (2026-07-10)

- Fix versioning.

## 0.1.0 (2026-07-09)

- Initial release of the project.
