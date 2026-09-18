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
5. Check netplan command exists
6. Configure sudo use_pty
7. Configure sudo logfile
8. Configure sudo disable pwfeedback
9. Configure sudo disable visiblepw
10. Configure sudo passwd_timeout
11. Configure sudo timestamp_timeout
12. Configure sudo timestamp_type
13. Configure sudo netplan command umask
14. Configure sudo to disable rootpw and targetpw
15. Configure sudo to disable runaspw
16. Create su group sugroup
17. Configure su group

When `/usr/sbin/netplan` is installed, the role configures a `0027` umask
only for that command. This preserves a restrictive global umask while
allowing generated `root:systemd-network` networkd configuration files to be
group-readable.

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
