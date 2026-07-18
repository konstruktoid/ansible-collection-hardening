# systemdconf

Ansible role to configure systemd system.conf and user.conf files.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/systemdconf/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `limit_nofile_hard` | `1024` | Maximum number of open files, hard resource limit |
| `limit_nproc_hard` | `1024` | Maximum number of processes, hard resource limit |
| `system_conf_template` | `"etc/systemd/system.conf.j2"` | systemd system.conf template location. |
| `user_conf_template` | `"etc/systemd/user.conf.j2"` | systemd user.conf template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Configure systemd system.conf
2. Configure systemd user.conf

## Handlers

- Reload systemd

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.systemdconf
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
