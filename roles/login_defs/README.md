# login_defs

Configure /etc/login.defs settings to enforce secure account and password policy defaults on supported Linux systems.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/login_defs/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `login_defs` | mapping, see below | login.defs configuration options. |
| `login_defs_template` | `"etc/login.defs.j2"` | /etc/login.defs template location. |

`login_defs` default value:

```yaml
home_mode: '0700'
login_retries: 5
login_timeout: 60
pass_max_days: 60
pass_min_days: 1
pass_min_length: 15
pass_warn_age: 7
umask_value: '0077'
usergroups_enabled: true
```

## Tasks

`tasks/main.yml` executes, in order:

1. Get PAM version
2. Gather package facts
3. Get libpam version in Debian family
4. Get libpam version in RedHat family
5. Set hashing algorithm for password (yescrypt|sha512)
6. Configure login.defs

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.login_defs
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
