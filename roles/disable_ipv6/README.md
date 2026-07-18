# disable_ipv6

Disable IPv6 by configuring the `net.ipv6.conf.*.disable_ipv6` sysctl keys and the GRUB kernel command line.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/disable_ipv6/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `ipv6_disable_sysctl_settings` | mapping, see below | IPv6 sysctl settings to disable IPv6. |
| `sysctl_disable_ipv6_template` | `"etc/sysctl/disable_ipv6.conf.j2"` | Template for sysctl settings to disable IPv6. |

`ipv6_disable_sysctl_settings` default value:

```yaml
net.ipv6.conf.all.disable_ipv6: 1
net.ipv6.conf.default.disable_ipv6: 1
```

## Tasks

`tasks/main.yml` executes, in order:

1. Set sysctl configuration directory as fact
2. Stat /usr/lib/sysctl.d/
3. Set /usr/lib/sysctl.d/ existence fact
4. Set sysctl_conf_dir fact based on /usr/lib/sysctl.d/ existence
5. Ensure sysctl configuration dir has the correct permissions
6. Sysctl settings for disabling IPv6
7. Set Debian ipv6.disable GRUB cmdline
8. Set RedHat ipv6.disable GRUB cmdline

## Handlers

- Restart sysctl
- Update GRUB

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.disable_ipv6
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
