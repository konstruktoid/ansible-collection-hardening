# journald

Configures systemd-journald storage, rotation, and file permissions; installs and configures rsyslog and logrotate for log forwarding and rotation; disables systemd-journal-remote.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/journald/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `journald_compress` | `true` | If True, journal files will be compressed. |
| `journald_conf_template` | `"etc/systemd/journald.conf.j2"` | systemd journald.conf template location. |
| `journald_forwardtosyslog` | `false` | If True, forward journal messages to syslog. |
| `journald_group` | `"systemd-journal"` | The group that has access to the journal files. |
| `journald_dir_mode` | `"2750"` | Default permissions journald directory permissions. |
| `journald_file_mode` | `"0640"` | Set the file creation mode for journal files. |
| `journald_storage` | `"persistent"` | Controls where to store journal data. |
| `journald_system_max_use` | `""` | How much disk space the journal may use up at most. |
| `journald_user` | `"root"` | The user that has access to the journal files. |
| `logrotate_conf_template` | `"etc/logrotate.conf.j2"` | logrotate.conf template location. |
| `rsyslog_filecreatemode` | `"0640"` | Set the file creation mode for rsyslog log files. |

## Tasks

`tasks/main.yml` executes, in order:

1. Configure systemd journald.conf
2. Probe systemd-journal-remote units
3. Disable systemd-journal-remote
4. Stat journald tmpfiles configuration directory
5. Set restrictive permissions on journal files
6. Apply journald tmpfiles permissions
7. Ensure logrotate and xz is installed on Debian-based systems
8. Ensure logrotate and xz is installed on RedHat-based systems
9. Configure logrotate(8)
10. Configure logrotate timers
11. Ensure rsyslog is installed on Debian-based systems
12. Ensure rsyslog is installed on RedHat-based systems
13. Stat rsyslog.conf
14. Stat rsyslog.d
15. Set rsyslog FileCreateMode
16. Manage FileCreateMode in rsyslog.conf
17. Add FileCreateMode drop-in to rsyslog.d

## Handlers

- Restart systemd-journald
- Validate rsyslogd
- Reload systemd
- Start daily-logrotate.timer

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.journald
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
