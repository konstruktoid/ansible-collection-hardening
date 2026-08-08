# Change Log

## Unreleased

- Remove the unused `sshd_admin_net` variable from the `ssh` role. It is a leftover from
  `ansible-role-hardening`, where the role also managed the firewall, and it has had no effect
  since firewalling moved to the separate `ufw` and `firewalld` roles. Use `ufw_admin_net` or
  `firewalld_admin_net` to restrict which networks may connect.
- Make the `timesyncd` role stop and disable any other time synchronization service, listed in
  the new `timesyncd_conflicting_services` variable, and drop the `timedatectl set-ntp` task.
  On AlmaLinux and Ubuntu, which ship `chrony`, the role previously left both clients enabled:
  `systemd-timedated` selects the first unit in `/usr/lib/systemd/ntp-units.d/`, where
  `50-chrony*` sorts before `80-systemd-timesync`, so `timedatectl set-ntp true` disabled
  `systemd-timesyncd` again, and `chronyd.service` (`Conflicts=systemd-timesyncd.service`,
  started after `sysinit.target`) stopped it on the next boot. The NTP servers configured by
  the role were therefore never used on those platforms.
- Stop the `apparmor` role from enforcing profiles that declare `flags=(unconfined)`,
  `flags=(prompt)` or `flags=(default_allow)`. Note that hosts hardened with an earlier
  release keep the rewritten profiles on disk and have to be restored separately, for example
  with `apt-get install --reinstall apparmor apparmor-profiles`.
- Set `lock_timeout` on the `apt` handlers in the `automatic_updates` and `packages` roles,
  so that cleanup no longer fails when a package management service still holds the apt lock.
- Install `epel-release` during test preparation instead of mid-play, and document that
  repository adding roles have to run before the upgrade, so that the repository set is
  stable across both converges and the idempotence check on AlmaLinux no longer fails.
- Add `file_permissions` role, restricting the ownership and permissions of the account
  databases (`/etc/passwd`, `/etc/shadow`, `/etc/group`, `/etc/gshadow`, their backup files
  and `/etc/security/opasswd`) and of the bootloader configuration files.
- Extend `packages_blocklist` with the network server packages that remote vulnerability
  scanners fingerprint and report on: DNS (`bind`, `bind9`, `dnsmasq`), SNMP (`net-snmp`,
  `snmpd`), NFS (`nfs-kernel-server`), print (`cups`, `cups-browsed`, `cups-daemon`), SMB
  (`samba`), LDAP (`openldap-servers`, `slapd`), IMAP/POP3 (`cyrus-imapd`, `dovecot`,
  `dovecot-core`), DHCP (`dhcp-server`, `isc-dhcp-server`), proxy (`squid`), VNC
  (`tigervnc-server`), NIS (`nis`, `ypserv`), the remaining cleartext r-services
  (`rsh-redone-client`, `rsh-redone-server`, `rusersd`, `rwho`), `rsync-daemon` and the
  remaining telnet and TFTP server package names (`inetutils-telnetd`, `telnetd`,
  `tftp-server`). Override `packages_blocklist` on hosts that legitimately run any of these.
- Add `chrony` role, configuring `chrony` as a client only NTP daemon and as the single time
  synchronization service on the host: NTS authenticated sources only, `authselectmode require`,
  `minsources 3`, no NTP port, no command port and no `sourcedir`/`confdir` includes, so that a
  DHCP server cannot add unauthenticated sources. Serving time is opt-in behind
  `chrony_server_enabled`. The role ships no systemd drop-in, the packaged units are already
  hardened. It is the alternative to the `timesyncd` role, apply one or the other.
  The role also installs `ca-certificates`, which is not a dependency of the `chrony` package on
  the Debian family: NTS is TLS, and without a trust store every NTS-KE handshake fails with
  `The certificate issuer is unknown` and the host never synchronizes its clock.
- Extend `timesyncd_conflicting_services` with `chronyd-restricted.service` and
  `ntpd-rs.service`, so that switching a host to `systemd-timesyncd` also stops the restricted
  `chronyd` variant both families package, and `ntpd-rs`, which Debian trixie packages.
- Converge and verify the `chrony` role instead of the `timesyncd` role in the Molecule
  scenarios. Both roles disable the other one, so only one of them can be tested per host, and
  `chrony` is what the supported platforms ship. `extensions/molecule/tests/verify_timesyncd.yml`
  is kept for scenarios that select `timesyncd` instead.

## 0.2.0 (2026-07-23)

- Add `firewalld` role.
- Add `llmr` and multicast sysctl options.
- Update collection support documentation to reflect what is actually supported.
- Harden GitHub Actions workflows (SLSA, least-privilege permissions, `author_association` gate).
- Add and update Claude Code verification loop tooling under `.claude/`.
- Remove Vagrant, dedup and improve testing.

## 0.1.1 (2026-07-10)

- Fix versioning.

## 0.1.0 (2026-07-09)

- Initial release of the project.
