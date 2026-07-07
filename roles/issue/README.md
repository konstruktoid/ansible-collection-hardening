# issue

Role to update /etc/issue and /etc/motd files using Jinja2 templates.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/issue/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `issue_template` | `"etc/issue.j2"` | /etc/issue template location. |
| `motd_template` | `"etc/motd.j2"` | /etc/motd template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Add motd file
2. Add issue and issue.net files

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.issue
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
