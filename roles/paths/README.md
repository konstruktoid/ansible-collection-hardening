# paths

PATH and environment hardening for AlmaLinux, Debian, and Ubuntu systems.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/paths/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `initpath_sh_template` | `"etc/profile.d/initpath.sh.j2"` | profile initpath.sh template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Set path
2. Add path script

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.paths
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
