# postfix

Ansible role to harden Postfix MTA.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

This role has no configurable variables.

## Tasks

`tasks/main.yml` executes, in order:

1. Install Postfix
2. Stat postfix main.cf
3. Configure Postfix
4. Configure Postfix disable_vrfy_command
5. Configure Postfix inet_interfaces
6. Configure Postfix smtpd_banner
7. Configure Postfix smtpd_client_restrictions
8. Configure Postfix smtpd_data_restrictions
9. Configure Postfix smtpd_discard_ehlo_keywords

## Handlers

- Restart Postfix

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.postfix
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
