# timesyncd

Ansible role to manage timesyncd configuration.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/timesyncd/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `fallback_ntp` | `["ntp.netnod.se", "ntp.ubuntu.com"]` | A list of NTP server host names or IP addresses to be used as the fallback NTP servers. |
| `ntp` | `["2.pool.ntp.org", "time.nist.gov"]` | A list of NTP server host names or IP addresses to be used as the primary NTP servers. |
| `timesyncd_conf_template` | `"etc/systemd/timesyncd.conf.j2"` | systemd timesyncd.conf template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Install and configure systemd timesyncd
2. Install epel-release for RHEL-based systems
3. Install systemd timesyncd
4. Configure systemd timesyncd
5. Start timesyncd
6. Stat timedatectl show
7. Run timedatectl set-ntp

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

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
