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
| `packages_blocklist` | `["apport", "autofs", "avahi", "beep", "ftp", "git", "inetutils-telnet", "pastebinit", "popularity-contest", "prelink", "rpcbind", "rsh", "rsh-server", "rsync", "talk", "telnet", "telnet-server", "tftp", "tftpd", "tnftp", "tuned", "vsftpd", "whoopsie", "xinetd", "yp-tools", "ypbind"]` | Packages that will be removed from the system if they are installed. |
| `packages_debian` | `["acct", "apparmor-profiles", "apparmor-utils", "apt-listchanges", "apt-show-versions", "audispd-plugins", "auditd", "cracklib-runtime", "curl", "debsums", "gnupg2", "libpam-apparmor", "libpam-cap", "libpam-modules", "libpam-tmpdir", "lsb-release", "needrestart", "openssh-server", "postfix", "rsyslog", "sysstat", "systemd-journal-remote", "tcpd", "vlock", "wamerican"]` | Packages to install on Debian-based systems. |
| `packages_redhat` | `["audispd-plugins", "audit", "cracklib", "curl", "gnupg2", "openssh-server", "postfix", "psacct", "python3-dnf-plugin-post-transaction-actions", "rsyslog", "rsyslog-gnutls", "systemd-journal-remote", "vlock", "words"]` | Packages to install on Red Hat-based systems. |
| `packages_ubuntu` | `["fwupd", "secureboot-db", "snapd"]` | Packages to install on Ubuntu-based systems. |

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
