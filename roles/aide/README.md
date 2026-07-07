# aide

Installation and configuration of AIDE (Advanced Intrusion Detection Environment) on Linux systems.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/aide/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `aide_checksums` | `"sha512"` | Modifies the AIDE `Checksums` variable. |
| `aide_dir_exclusions` | `["/var/lib/docker", "/var/lib/lxcfs", "/var/lib/private/systemd", "/var/log/audit", "/var/log/journal"]` | AIDE directories to exclude from checks. |

## Tasks

`tasks/main.yml` executes, in order:

1. AIDE installation and configuration
2. Debian family AIDE installation
3. RedHat family AIDE package installation
4. Stat AIDE cron.daily
5. Install AIDE service
6. Install AIDE timer
7. Configure AIDE checksums
8. Get AIDE include config
9. Set AIDE include directory as fact
10. Check if AIDE include directory exists
11. Add auditd tools
12. Add AIDE dir exclusions
13. Add auditd tools in include directory
14. Add AIDE dir exclusions
15. Stat Debian aide.db
16. Stat RedHat aide.db
17. Initialize RedHat AIDE
18. Stat RedHat aide.db.new.gz
19. Copy RedHat AIDE database
20. Initialize Debian AIDE

## Handlers

- Reload systemd
- Enable aidecheck
- Disable aidecheck
- Mask aidecheck

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.aide
```

## Tags

`aide`, `almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
