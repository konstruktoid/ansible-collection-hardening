# tcpwrappers

tcpwrappers, hosts.allow and hosts.deny, management.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/tcpwrappers/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `hosts_allow_template` | `"etc/hosts.allow.j2"` | /etc/hosts.allow template location. |
| `hosts_deny_template` | `"etc/hosts.deny.j2"` | /etc/hosts.deny template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Configure hosts.allow
2. Configure hosts.deny

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.tcpwrappers
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
