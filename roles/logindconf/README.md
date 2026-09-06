# logindconf

Configure systemd-logind settings by managing a `logind.conf.d` drop-in file.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/logindconf/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `logind_conf_template` | `"etc/systemd/logind.conf.j2"` | systemd logind.conf template location. |
| `logindconf_logind` | mapping, see below | Configure systemd-logind settings. |
| `logindconf_session_timeout` | `900` | Sets, in seconds, the StopIdleSessionSec if systemd version 252 or newer |

`logindconf_logind` default value:

```yaml
killuserprocesses: true
killexcludeusers:
- root
idleaction: lock
idleactionsec: 15min
removeipc: true
```

## Tasks

`tasks/main.yml` executes, in order:

1. Configure systemd logind
2. Create logind.conf.d drop-in directory
3. Configure systemd logind

## Handlers

- Restart systemd-logind

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.logindconf
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
