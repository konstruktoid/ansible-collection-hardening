# chrony

Ansible role to manage chrony configuration.

The role configures chrony as a client only NTP daemon: it does not open the NTP port, it does
not open the command port, and every time source it configures is authenticated with
[Network Time Security](https://datatracker.ietf.org/doc/html/rfc8915). Serving time to other
hosts is possible, but it is strictly opt-in, see `chrony_server_enabled`.

Any other time synchronization service, listed in `chrony_conflicting_services`, is stopped and
disabled so that chrony is the only service synchronizing the system clock. This is the same
mutual exclusion the [`timesyncd`](../timesyncd/README.md) role does in the other direction, and
running either role last leaves the host with a single time source. The two roles are
alternatives, do not apply both to the same host and expect both to keep running.

The default sources, `time.cloudflare.com`, `ntppool1.time.nl`, `nts.netnod.se` and
`ptbtime1.ptb.de`, are a supply chain decision and not only a time decision: they are the
organizations a host asks what time it is, and they see the host asking. Review
`chrony_sources` before using the defaults.

`chrony_authselectmode` is `require` by default, which means chronyd refuses to select a source
that is not authenticated. Every default source supports NTS, so this changes nothing until an
unauthenticated source is added, and the role then fails the run rather than letting the host
fall back to spoofable time. On a network that filters outbound 4460/tcp, or on a host that
comes up with a clock too wrong to validate a certificate, it turns a degraded synchronization
into no synchronization at all. `chrony_nocerttimecheck` handles the second case, and setting
`chrony_authselectmode` to `ignore` handles the first.

The NTP port, 123/udp, and the NTS-KE port, 4460/tcp, are managed by the
[`ufw`](../ufw/README.md) and [`firewalld`](../firewalld/README.md) roles, not by this one.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/chrony/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `chrony_authselectmode` | `"require"` | Authentication required for a source to be selected. `require` rejects every unauthenticated source, `ignore` is the chronyd default. Set to an empty string to leave the directive out. |
| `chrony_cmdport` | `0` | UDP port chronyd listens on for chronyc command packets. `0` disables it, chronyc still works for root over the Unix domain socket. |
| `chrony_conf` | `"/etc/chrony/chrony.conf"` on the Debian family, `"/etc/chrony.conf"` otherwise | Path of the chrony configuration file. |
| `chrony_conf_mode` | `"0644"` | File mode of the chrony configuration file. |
| `chrony_conf_template` | `"etc/chrony/chrony.conf.j2"` | chrony.conf template location. |
| `chrony_confdirs` | `[]` | Directories scanned for additional configuration files, `confdir` directives. |
| `chrony_conflicting_services` | `["systemd-timesyncd.service", "ntp.service", "ntpd.service", "ntpsec.service", "openntpd.service", "ntpd-rs.service", "chronyd-restricted.service"]` | Services that also synchronize the system clock. They are stopped and disabled so that chrony is the only time synchronization service on the host. |
| `chrony_driftfile` | `"/var/lib/chrony/chrony.drift"` on the Debian family, `"/var/lib/chrony/drift"` otherwise | File in which chronyd records the rate at which the system clock gains or loses time. |
| `chrony_dumpdir` | `"/run/chrony"` | Directory in which chronyd saves the measurement history. |
| `chrony_group` | `"_chrony"` on the Debian family, `"chrony"` otherwise | Group of the chrony daemon user. |
| `chrony_leapseclist` | `"/usr/share/zoneinfo/leap-seconds.list"` | File containing the TAI-UTC offset and the leap seconds. The directive is only written when the file exists on the target. |
| `chrony_logdir` | `"/var/log/chrony"` | Directory in which chronyd writes its log files. |
| `chrony_makestep` | `"1.0 3"` | Step the clock instead of slewing it if the correction is larger than the first value, for the first number of updates given by the second value. |
| `chrony_minsources` | `3` | Minimum number of selectable sources required to adjust the system clock. |
| `chrony_noclientlog` | `true` | If True, no per client access logs are kept. |
| `chrony_nocerttimecheck` | `0` | Number of clock updates for which the NTS-KE certificate time checks are disabled. `0` keeps the checks. |
| `chrony_ntsdumpdir` | `"/var/lib/chrony"` | Directory in which chronyd saves NTS keys and cookies. |
| `chrony_ntsprocesses` | `1` | Number of helper processes handling NTS-KE sessions. |
| `chrony_ntsservercert` | `"/etc/chrony/nts-server.crt"` on the Debian family, `"/etc/pki/tls/certs/chrony-nts.crt"` otherwise | Certificate, or certificate chain, presented to NTS clients. |
| `chrony_ntsservercert_mode` | `"0644"` | File mode of `chrony_ntsservercert`. |
| `chrony_ntsserverkey` | `"/etc/chrony/nts-server.key"` on the Debian family, `"/etc/pki/tls/private/chrony-nts.key"` otherwise | Private key of the NTS server certificate. |
| `chrony_ntsserverkey_mode` | `"0640"` | File mode of `chrony_ntsserverkey`. It is owned by root and readable by `chrony_group`. |
| `chrony_packages` | `["chrony", "ca-certificates"]` | Packages required to synchronize the clock over NTS. |
| `chrony_port` | `0` | UDP port chronyd listens on for NTP requests. `0` means the host is a client only. |
| `chrony_ratelimit_burst` | `16` | Number of requests a client may send faster than `chrony_ratelimit_interval` before chronyd starts dropping them. |
| `chrony_ratelimit_interval` | `1` | Interval, as a power of two seconds, between responses to a client before chronyd starts dropping requests. |
| `chrony_rtconutc` | `false` | If True, the real time clock is assumed to keep UTC. Wrong for hosts that dual boot an operating system that keeps local time in the RTC. |
| `chrony_rtcsync` | `true` | If True, the real time clock is synchronized from the system clock every 11 minutes. |
| `chrony_server_allow` | `[]` | Networks allowed to use the host as a time source, `allow` directives. An empty list serves nobody. |
| `chrony_server_enabled` | `false` | If True, the host serves time to the networks listed in `chrony_server_allow`. It requires `chrony_port` to be a real port. |
| `chrony_service` | `"chrony.service"` on the Debian family, `"chronyd.service"` otherwise | Name of the chrony systemd unit. |
| `chrony_sourcedirs` | `[]` | Directories scanned for additional source files, `sourcedir` directives. |
| `chrony_sources` | `[{"address": "time.cloudflare.com", "type": "server", "options": ["iburst", "nts"]}, {"address": "ntppool1.time.nl", "type": "server", "options": ["iburst", "nts"]}, {"address": "nts.netnod.se", "type": "server", "options": ["iburst", "nts"]}, {"address": "ptbtime1.ptb.de", "type": "server", "options": ["iburst", "nts"]}]` | Time sources. Every source is emitted as `<type> <address> <options>`. |
| `chrony_user` | `"_chrony"` on the Debian family, `"chrony"` otherwise | User chronyd drops its privileges to. |

## Notes

`ca-certificates` is installed together with `chrony`. It is not a dependency of the `chrony`
package on the Debian family, and NTS is TLS: without a trust store every NTS-KE handshake fails
with `The certificate issuer is unknown`, and `authselectmode require` then leaves the host with
`Can't synchronise: no selectable sources`.

`chrony_sourcedirs` and `chrony_confdirs` are empty by default, which means the packaged
`sourcedir /run/chrony-dhcp`, `sourcedir /etc/chrony/sources.d` and `confdir /etc/chrony/conf.d`
includes are not written. The configuration of a host is then the single file this role manages.
On Ubuntu that also means the `sources.d` NTS pools and the `conf.d` bootstrap CA the package
ships are no longer read. Add the directories back if you want them.

The systemd units the distributions ship for chrony already set `ProtectSystem=strict`,
`ProtectProc=invisible`, `MemoryDenyWriteExecute=yes`, `PrivateTmp=yes`, `DevicePolicy=closed`,
`SystemCallFilter`, a trimmed `CapabilityBoundingSet` and dedicated
`RuntimeDirectory`/`StateDirectory`/`LogsDirectory` entries. The role therefore ships no drop-in:
there is nothing left worth adding that does not also break the reference clock, RTC or
`mailonchange` paths those units deliberately keep open.

On the Debian family, the AppArmor profile shipped with the package only lets chronyd read
`/etc/chrony/**` and `/etc/chrony.*`. An NTS server key or certificate has to be placed under
`/etc/chrony` there, and the configuration cannot be validated through the `validate` argument of
the template module, since chronyd may not read the temporary file it creates. The role writes
the configuration, keeps a backup, parses it with `chronyd -p` and restores the backup when
chronyd rejects it.

## Tasks

`tasks/main.yml` executes, in order:

1. Install and configure chrony
2. Assert that the time sources are usable
3. Assert that every time source is authenticated
4. Assert that a time server accepts NTP requests
5. Install chrony
6. Stat the leap second list
7. Set the NTS server key and certificate ownership and permissions
8. Configure chrony
9. Validate the chrony configuration
10. Parse the chrony configuration
11. Restore the previous chrony configuration
12. Fail because chronyd rejected the configuration
13. Gather service facts
14. Stop conflicting time synchronization services
15. Disable conflicting time synchronization services
16. Start chrony

## Handlers

- Restart chrony

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.chrony
```

## Tags

`almalinux`, `chrony`, `cis`, `debian`, `disa`, `hardening`, `ntp`, `security`, `system`, `ubuntu`

## License

Apache-2.0
