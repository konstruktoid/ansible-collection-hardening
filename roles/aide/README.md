# aide

Installation and configuration of AIDE (Advanced Intrusion Detection Environment) on Linux systems.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

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
5. Stat AIDE package timer
6. Install AIDE service
7. Install AIDE timer
8. Configure AIDE checksums
9. Get AIDE include config
10. Set AIDE include directory as fact
11. Check if AIDE include directory exists
12. Add auditd tools
13. Add AIDE dir exclusions
14. Add auditd tools in include directory
15. Add AIDE dir exclusions
16. Stat Debian aide.db
17. Stat RedHat aide.db
18. Initialize RedHat AIDE
19. Stat RedHat aide.db.new.gz
20. Copy RedHat AIDE database
21. Initialize Debian AIDE

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

`aide`, `almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
