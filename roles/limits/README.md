# limits

Configures PAM resource limits in `/etc/security/limits.conf` and systemd-coredump behavior in `coredump.conf`; disables the kdump crash-dump service.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/limits/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `coredump_conf_template` | `"etc/systemd/coredump.conf.j2"` | systemd coredump.conf template location. |
| `limit_nofile_hard` | `1024` | Maximum number of open files, hard resource limit |
| `limit_nofile_soft` | `512` | Maximum number of open files, soft resource limit |
| `limit_nproc_hard` | `1024` | Maximum number of processes, hard resource limit |
| `limit_nproc_soft` | `512` | Maximum number of processes, soft resource limit |
| `limits_conf_template` | `"etc/security/limits.conf.j2"` | limits.conf template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Configure limits.conf
2. Configure coredump.conf
3. Disable kdump service

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.limits
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
