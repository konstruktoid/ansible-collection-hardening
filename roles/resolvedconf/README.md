# resolvedconf

systemd-resolved configuration.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/resolvedconf/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `dns` | `["1.1.1.2", "9.9.9.9"]` | A list of addresses to use as system DNS servers. |
| `dns_over_tls` | `"opportunistic"` | Set the DNS over TLS mode for systemd-resolved. |
| `dnssec` | `"allow-downgrade"` | Set the DNSSEC mode for systemd-resolved. |
| `fallback_dns` | `["1.0.0.2", "149.112.112.112"]` | A list of addresses to use as the fallback DNS servers. |
| `resolved_conf_template` | `"etc/systemd/resolved.conf.j2"` | Systemd resolved.conf template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Install systemd-resolved
2. Install systemd-resolved
3. Configure systemd resolved
4. Ensure configuration is active
5. Reload systemd
6. Restart resolved service

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.resolvedconf
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
