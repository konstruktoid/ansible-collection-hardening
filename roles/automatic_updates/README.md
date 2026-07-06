# automatic_updates

Configure unattended-upgrades to automatically install security updates.

## Requirements

- Ansible-core >= 2.18
- `community.general` collection

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/automatic_updates/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `automatic_updates` | mapping, see below | Configure automatic updates. |
| `unattended_upgrades_custom_origins_template` | `"etc/apt/apt.conf.d/53unattended-upgrades-custom-origins.j2"` | APT unattended-upgrades for custom origins template location. |
| `unattended_upgrades_template` | `"etc/apt/apt.conf.d/52unattended-upgrades-local.j2"` | APT unattended-upgrades template location. |

`automatic_updates` default value:

```yaml
only_security: true
reboot: false
reboot_from_time: '2:00'
reboot_time_margin_mins: 20
custom_origins: []
```

## Tasks

`tasks/main.yml` executes, in order:

1. Install and configure dnf-automatic
2. Install dnf-automatic
3. Install updates automatically
4. Install only security updates
5. Configure reboot after updates
6. Enable dnf-automatic timer
7. Install and configure unattended-upgrades
8. Install unattended-upgrades
9. Configure unattended-upgrades package lists updates
10. Configure unattended-upgrades upgrade interval
11. Set base time and margin for reboot calculation
12. Calculate random margin
13. Calculate total minutes for reboot
14. Translates to hours, and minutes
15. Configure unattended-upgrades
16. Configure unattended-upgrades for custom_origins
17. Remove unattended-upgrades custom origins config when not in use
18. Check if unattended-upgrades service exists
19. Enable and start unattended-upgrades service

## Handlers

- Restart unattended-upgrades
- Run apt-get clean
- Run apt-get autoremove
- Run dnf autoremove

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.automatic_updates
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
