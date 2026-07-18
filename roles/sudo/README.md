# sudo

SUDO configuration and hardening.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/sudo/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `sudo_logfile` | `"/var/log/sudo.log"` | Path to the sudo log file. |
| `sudo_passwd_timeout` | `1` | Number of minutes before sudo prompts for a password again. |
| `sudo_timestamp_timeout` | `5` | Number of minutes sudo credential caching remains valid. |

## Tasks

`tasks/main.yml` executes, in order:

1. Configure sudo
2. Ensure sudo is installed
3. Check sudo type
4. Set fact for sudo type
5. Configure sudo use_pty
6. Configure sudo logfile
7. Configure sudo disable pwfeedback
8. Configure sudo disable visiblepw
9. Configure sudo passwd_timeout
10. Configure sudo timestamp_timeout
11. Configure sudo timestamp_type
12. Configure sudo to disable rootpw and targetpw
13. Configure sudo to disable runaspw
14. Create su group sugroup
15. Configure su group

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.sudo
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `sudo`, `ubuntu`

## License

Apache-2.0
