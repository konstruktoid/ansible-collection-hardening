# auditd

Install and configure auditd and manage audit rules on AlmaLinux, Debian, and Ubuntu.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/auditd/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `auditd_action_mail_acct` | `"root"` | This option should contain a valid email address or alias. |
| `auditd_admin_space_left_action` | `"suspend"` | This parameter tells the system what action to take when the system has detected that it is starting to get low on disk space. |
| `auditd_apply_audit_rules` | `true` | If True, the role applies the auditd rules from the included template file. |
| `auditd_disk_error_action` | `"suspend"` | This parameter tells the system what action to take whenever there is an error detected when writing audit events to disk or rotating logs. |
| `auditd_disk_full_action` | `"suspend"` | This parameter tells the system what action to take when the system has detected that the partition to which log files are written has become full. |
| `auditd_enable_flag` | `2` | Set enabled flag for auditd service. |
| `auditd_flush` | `"incremental_async"` | When to flush the audit records to disk. |
| `auditd_ignore_errors` | `false` | If True, the audit daemon will ignore errors when reading rules from a file. |
| `auditd_max_log_file` | `20` | This keyword specifies the maximum file size in megabytes. When this limit is reached, it will trigger a configurable action. |
| `auditd_max_log_file_action` | `"rotate"` | This parameter tells the system what action to take when the system has detected that the max file size limit has been reached. |
| `auditd_mode` | `1` | Set failure mode. |
| `auditd_num_logs` | `5` | Specifies the number of log files to keep if rotate is given as the max_log_file_action. |
| `auditd_space_left` | `75` | If the free space in the filesystem containing log_file drops below this value (in mb), the audit daemon takes the action specified by space_left_action. |
| `auditd_space_left_action` | `"email"` | This parameter tells the system what action to take when the system has detected that it is starting to get low on disk space. |
| `grub_audit_backlog_cmdline` | `"audit_backlog_limit=8192"` | Set the audit backlog limit in the GRUB command line. |
| `grub_audit_cmdline` | `"audit=1"` | Enable auditd in the GRUB command line. |
| `hardening_rules_template` | `"etc/audit/rules.d/hardening.rules.j2"` | auditd rules template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Configure auditd
2. Install audit package
3. Install initscripts
4. Install audit-rules
5. Ensure /etc/audit/rules.d exists
6. Configure Debian auditd GRUB cmdline
7. Configure RedHat auditd GRUB cmdline
8. Configure auditd action_mail_acct
9. Configure auditd admin_space_left_action
10. Configure auditd disk_error_action
11. Configure auditd disk_full_action
12. Configure auditd flush
13. Configure auditd max_log_file
14. Configure auditd max_log_file_action
15. Configure auditd num_logs
16. Configure auditd space_left
17. Configure auditd space_left_action
18. Configure auditd name_format
19. Enable auditd syslog plugin
20. Add auditd rules

## Handlers

- Generate auditd rules
- Enable auditd
- Update GRUB

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.auditd
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
