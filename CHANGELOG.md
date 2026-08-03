# Change Log

## Unreleased

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
