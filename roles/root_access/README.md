# root_access

Limit root access using /etc/securetty, /etc/security/access.conf and masking debug-shell.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

This role has no configurable variables.

## Tasks

`tasks/main.yml` executes, in order:

1. Stat and manage /etc/security/access.conf
2. Stat access.conf
3. Remove non-standard root entries from access.conf
4. Configure root access entries in access.conf
5. Disable root TTY logins via /etc/securetty
6. Ensure /etc/securetty is empty
7. Gather debug-shell.service systemd unit status
8. Mask systemd debug-shell

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.root_access
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
