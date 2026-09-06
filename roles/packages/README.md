# packages

Ansible role to manage packages on Debian and RHEL based systems.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/packages/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `packages_needrestart_disable_interpscan` | `true` | If True, disable needrestart's interpreter scanners (Python, Ruby, etc.), which have been affected by local privilege escalation vulnerabilities such as CVE-2024-48990 and CVE-2024-48991. |
| `packages_blocklist` | `["apport", "autofs", "avahi", "beep", "bind", "bind9", "cups", "cups-browsed", "cups-daemon", "cyrus-imapd", "dhcp-server", "dnsmasq", "dovecot", "dovecot-core", "ftp", "git", "inetutils-telnet", "inetutils-telnetd", "isc-dhcp-server", "net-snmp", "nfs-kernel-server", "nis", "openldap-servers", "pastebinit", "popularity-contest", "prelink", "rpcbind", "rsh", "rsh-redone-client", "rsh-redone-server", "rsh-server", "rsync", "rsync-daemon", "rusersd", "rwho", "samba", "slapd", "snmpd", "squid", "talk", "telnet", "telnet-server", "telnetd", "tftp", "tftp-server", "tftpd", "tigervnc-server", "tnftp", "tuned", "vsftpd", "whoopsie", "xinetd", "yp-tools", "ypbind", "ypserv"]` | Packages that will be removed from the system if they are installed. |
| `packages_debian` | `["acct", "apparmor-profiles", "apparmor-utils", "apt-listchanges", "apt-show-versions", "audispd-plugins", "auditd", "cracklib-runtime", "curl", "debsums", "gnupg2", "libpam-apparmor", "libpam-cap", "libpam-modules", "libpam-tmpdir", "lsb-release", "needrestart", "openssh-server", "postfix", "rsyslog", "sysstat", "systemd-journal-remote", "tcpd", "vlock", "wamerican"]` | Packages to install on Debian-based systems. |
| `packages_redhat` | `["audispd-plugins", "audit", "cracklib", "curl", "gnupg2", "openssh-server", "postfix", "psacct", "python3-dnf-plugin-post-transaction-actions", "rsyslog", "rsyslog-gnutls", "systemd-journal-remote", "vlock", "words"]` | Packages to install on Red Hat-based systems. |
| `packages_ubuntu` | `["fwupd", "secureboot-db", "snapd"]` | Packages to install on Ubuntu-based systems. |

`packages_blocklist` contains the network server and legacy cleartext packages
that remote vulnerability scanners fingerprint and report on: DNS, SNMP, NFS,
print, SMB, LDAP, IMAP/POP3, DHCP, proxy, VNC and NIS servers, the r-services,
and the telnet, FTP, TFTP and rsync daemons. Both the Debian and the Red Hat
package names are listed, so that the same blocklist applies on either family.

Removal is unconditional: a host that legitimately provides one of these
services must override `packages_blocklist` and drop the relevant entries,
otherwise the role removes the package and the service with it.

## Tasks

`tasks/main.yml` executes, in order:

1. Gather the package facts
2. Intersect installed packages with blocklist
3. Generic package removal
4. Debian family package management
5. Debian family package installation
6. Ubuntu package installation
7. Install unattended-upgrades support package
8. Run apt purge
9. RedHat family package installation
10. VirtualBox guest packages installation
11. VMWare package installation
12. QEMU package installation
13. Install and start rngd
14. Install rngd
15. Start and enable rngd service
16. Stat sysstat default
17. Enable sysstat
18. Remove unneeded Debian dependencies
19. Run dnf autoremove
20. Populate package facts
21. Populate service facts
22. Configure needrestart
23. Pre register needrestart configuration directory
24. Create needrestart directory
25. Stat needrestart configuration directory
26. Get needrestart restart value
27. Configure needrestart

## Handlers

- Run apt-get clean
- Run apt-get autoremove
- Run dnf autoremove

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.packages
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
