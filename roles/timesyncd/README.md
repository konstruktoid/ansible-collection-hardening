# timesyncd

Ansible role to manage timesyncd configuration.

Any other time synchronization service, listed in `timesyncd_conflicting_services`, is stopped
and disabled so that `systemd-timesyncd` is the only service synchronizing the system clock.
This matters on distributions that ship a different NTP client by default, for example
AlmaLinux and Ubuntu, where `chrony` otherwise takes over the clock again after a reboot and
the servers configured by this role are never used.

The [`chrony`](../chrony/README.md) role is the alternative, and does the same mutual exclusion in
the other direction. The two roles are alternatives, do not apply both to the same host and
expect both to keep running.

On the Red Hat family `systemd-timesyncd` is only available from EPEL, so the role installs
`epel-release`. Roles that add repositories have to run before any package upgrade, see the
[`package_management`](../package_management/README.md) role.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/timesyncd/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `fallback_ntp` | `["ntp.netnod.se", "ntp.ubuntu.com"]` | A list of NTP server host names or IP addresses to be used as the fallback NTP servers. |
| `ntp` | `["2.pool.ntp.org", "time.nist.gov"]` | A list of NTP server host names or IP addresses to be used as the primary NTP servers. |
| `timesyncd_conf_template` | `"etc/systemd/timesyncd.conf.j2"` | systemd timesyncd.conf template location. |
| `timesyncd_conflicting_services` | `["chrony.service", "chronyd-restricted.service", "chronyd.service", "ntp.service", "ntpd-rs.service", "ntpd.service", "ntpsec.service", "openntpd.service"]` | Services that also synchronize the system clock. They are stopped and disabled so that systemd-timesyncd is the only time synchronization service on the host. |

## Tasks

`tasks/main.yml` executes, in order:

1. Install and configure systemd timesyncd
2. Install epel-release for RHEL-based systems
3. Install systemd timesyncd
4. Configure systemd timesyncd
5. Gather service facts
6. Stop conflicting time synchronization services
7. Disable conflicting time synchronization services
8. Start timesyncd

## Handlers

- Reload systemd
- Restart systemd-timesyncd

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.timesyncd
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
