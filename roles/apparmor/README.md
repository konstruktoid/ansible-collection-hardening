# apparmor

AppArmor installation and configuration.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| Ubuntu | resolute |

## Role variables

Defined in `roles/apparmor/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `apparmor_sysctl_settings` | mapping, see below | AppArmor sysctl settings. |
| `sysctl_apparmor_config_template` | `"etc/sysctl/sysctl.apparmor.conf.j2"` | AppArmor sysctl configuration template location. |

`apparmor_sysctl_settings` default value:

```yaml
kernel.apparmor_display_secid_mode: 0
kernel.apparmor_restrict_unprivileged_io_uring: 1
kernel.apparmor_restrict_unprivileged_unconfined: 1
kernel.apparmor_restrict_unprivileged_userns: 1
kernel.apparmor_restrict_unprivileged_userns_complain: 0
kernel.apparmor_restrict_unprivileged_userns_force: 1
kernel.unprivileged_userns_apparmor_policy: 1
```

## Tasks

`tasks/main.yml` executes, in order:

1. Set sysctl configuration directory as fact
2. Stat /usr/lib/sysctl.d/ exists
3. Set sysctl fact
4. Determine sysctl configuration directory
5. Print sysctl configuration directory
6. Configure and enable AppArmor
7. Install AppArmor packages
8. AppArmor sysctl settings
9. Set Debian family AppArmor grub cmdline
10. Configure pam_apparmor
11. Get AppArmor status
12. Enforce AppArmor profiles
13. Enable apparmor

## Handlers

- Restart sysctl
- Update GRUB

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.apparmor
```

## Tags

`cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
