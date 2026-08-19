# Ansible collection for Server Hardening

Ansible collection for hardening systemd-based Linux servers: AlmaLinux, Debian,
and Ubuntu. It applies CIS Benchmark- and DISA STIG-aligned security controls
through 44 independent, single-purpose roles covering SSH, sudo, PAM,
auditd, sysctl, firewalling, mounts, and kernel modules, among other hardening
domains.

Conversion of [ansible-role-hardening](https://github.com/konstruktoid/ansible-role-hardening)
to collection format.

See [OVERVIEW.md](OVERVIEW.md) for a high-level overview of the repository's
purpose, components, and scope.

See [PRESCRYB.md](PRESCRYB.md) for how to use
[`prescryb`](https://github.com/konstruktoid/prescryb), a companion MCP
server, to scan a hardened host for outstanding CVEs and compliance gaps
and get Ansible remediation suggestions referencing this collection's
roles.

## Requirements

- ansible-core >= 2.18.0

Some roles require the following additional collections:

| Collection | Minimum version | Required by |
| --- | --- | --- |
| `ansible.posix` | 2.2.0 | firewalld, mount, selinux, ufw |
| `community.crypto` | 3.2.1 | ssh |
| `community.general` | 13.0.1 | automatic_updates, disable_wireless, firewalld, ssh, ufw |

Install them with:

```console
ansible-galaxy collection install -r requirements.yml
```

## Supported platforms

| Platform | Versions |
| --- | --- |
| AlmaLinux / EL | 10 |
| Debian | trixie |
| Ubuntu | resolute |

Platform support is declared per role in `roles/<role>/meta/main.yml` and is
verified in CI against AlmaLinux 10, Debian trixie, and Ubuntu resolute
container images (`extensions/molecule/docker/molecule.yml`).

## Installation

```console
ansible-galaxy collection install konstruktoid.hardening
```

Or add it to `requirements.yml`:

```yaml
collections:
  - name: konstruktoid.hardening
```

## Usage

Apply a single role:

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.ssh
```

Apply the full collection by including every role in `roles/`. Each role is
independent and configured exclusively through its own variables in
`roles/<role>/defaults/main.yml`; there is no top-level playbook or umbrella
role. See each role's `README.md` for its variables and example usage.

## Roles

| Role | Description | Platforms |
| --- | --- | --- |
| [`adduser`](roles/adduser/README.md) | Configure adduser and useradd. | Debian, AlmaLinux/EL, Ubuntu |
| [`aide`](roles/aide/README.md) | Installation and configuration of AIDE (Advanced Intrusion Detection Environment) on Linux systems. | Debian, AlmaLinux/EL, Ubuntu |
| [`apparmor`](roles/apparmor/README.md) | AppArmor installation and configuration. | Debian, Ubuntu |
| [`apport`](roles/apport/README.md) | Manage Apport. | Debian, Ubuntu |
| [`auditd`](roles/auditd/README.md) | Install and configure auditd and manage audit rules on AlmaLinux, Debian, and Ubuntu. | Debian, AlmaLinux/EL, Ubuntu |
| [`automatic_updates`](roles/automatic_updates/README.md) | Configure unattended-upgrades to automatically install security updates. | Debian, AlmaLinux/EL, Ubuntu |
| [`chrony`](roles/chrony/README.md) | Ansible role to manage chrony configuration. | Debian, AlmaLinux/EL, Ubuntu |
| [`compilers`](roles/compilers/README.md) | Restrict compiler binaries to root on AlmaLinux, Debian, and Ubuntu systems. | Debian, AlmaLinux/EL, Ubuntu |
| [`ctrlaltdel`](roles/ctrlaltdel/README.md) | Disable Ctrl+Alt+Del key sequence to prevent reboots. | Debian, AlmaLinux/EL, Ubuntu |
| [`delete_users`](roles/delete_users/README.md) | Delete listed users. | Debian, AlmaLinux/EL, Ubuntu |
| [`disable_ipv6`](roles/disable_ipv6/README.md) | Disable IPv6 by configuring the `net.ipv6.conf.*.disable_ipv6` sysctl keys and the GRUB kernel command line. | Debian, AlmaLinux/EL, Ubuntu |
| [`disable_wireless`](roles/disable_wireless/README.md) | Disable wireless interfaces and wireless kernel modules on AlmaLinux, Debian, and Ubuntu systems. | Debian, AlmaLinux/EL, Ubuntu |
| [`file_permissions`](roles/file_permissions/README.md) | Restrict the ownership and permissions of the account databases and of the bootloader configuration files. | Debian, AlmaLinux/EL, Ubuntu |
| [`firewalld`](roles/firewalld/README.md) | An Ansible role to manage firewalld default-deny zone rules. | AlmaLinux/EL |
| [`issue`](roles/issue/README.md) | Role to update /etc/issue and /etc/motd files using Jinja2 templates. | Debian, AlmaLinux/EL, Ubuntu |
| [`journald`](roles/journald/README.md) | Configures systemd-journald storage, rotation, and file permissions; installs and configures rsyslog and logrotate for log forwarding and rotation; disables systemd-journal-remote. | Debian, AlmaLinux/EL, Ubuntu |
| [`kernel`](roles/kernel/README.md) | Hardens kernel runtime behavior via sysctl and boot-time parameters: restricts virtual syscalls (vsyscall), enables page poisoning, kernel page-table isolation, SLUB debug poisoning, and kernel lockdown mode, using GRUB or grubby depending on the platform. | Debian, AlmaLinux/EL, Ubuntu |
| [`kernel_modules`](roles/kernel_modules/README.md) | Kernel module blocklist/blacklist management for AlmaLinux, Debian and Ubuntu. | Debian, AlmaLinux/EL, Ubuntu |
| [`limits`](roles/limits/README.md) | Configures PAM resource limits in `/etc/security/limits.conf` and systemd-coredump behavior in `coredump.conf`; disables the kdump crash-dump service. | Debian, AlmaLinux/EL, Ubuntu |
| [`lock_root`](roles/lock_root/README.md) | Lock the root account and remove root SSH authorized_keys. | Debian, AlmaLinux/EL, Ubuntu |
| [`login_defs`](roles/login_defs/README.md) | Configure /etc/login.defs settings to enforce secure account and password policy defaults on supported Linux systems. | Debian, AlmaLinux/EL, Ubuntu |
| [`logindconf`](roles/logindconf/README.md) | Configure systemd-logind settings by managing a `logind.conf.d` drop-in file. | Debian, AlmaLinux/EL, Ubuntu |
| [`motd_news`](roles/motd_news/README.md) | Manage apt esm, motd-news and Ubuntu PRO. | Debian, Ubuntu |
| [`mount`](roles/mount/README.md) | Manage /dev/shm, /proc and /tmp mounts. | Debian, AlmaLinux/EL, Ubuntu |
| [`netplan`](roles/netplan/README.md) | Ensure netplan configuration permissions. | Debian, AlmaLinux/EL, Ubuntu |
| [`package_management`](roles/package_management/README.md) | Role to manage configuration of APT and DNF. | Debian, AlmaLinux/EL, Ubuntu |
| [`packages`](roles/packages/README.md) | Ansible role to manage packages on Debian and RHEL based systems. | Debian, AlmaLinux/EL, Ubuntu |
| [`password_management`](roles/password_management/README.md) | Configures PAM (`common-auth`, `common-account`, `common-password`, `faillock`, `pwquality`) and system-wide crypto-policies to enforce password quality requirements, hashing algorithm, account lockout, and FIPS mode. | Debian, AlmaLinux/EL, Ubuntu |
| [`paths`](roles/paths/README.md) | PATH and environment hardening for AlmaLinux, Debian, and Ubuntu systems. | Debian, AlmaLinux/EL, Ubuntu |
| [`postfix`](roles/postfix/README.md) | Ansible role to harden Postfix MTA. | Debian, AlmaLinux/EL, Ubuntu |
| [`prelink`](roles/prelink/README.md) | Disable prelink/prelinking on AlmaLinux, Debian, and Ubuntu systems. | Debian, AlmaLinux/EL, Ubuntu |
| [`resolvedconf`](roles/resolvedconf/README.md) | systemd-resolved configuration. | Debian, AlmaLinux/EL, Ubuntu |
| [`root_access`](roles/root_access/README.md) | Limit root access using /etc/securetty, /etc/security/access.conf and masking debug-shell. | Debian, AlmaLinux/EL, Ubuntu |
| [`schedulers`](roles/schedulers/README.md) | Configure scheduled command services. | Debian, AlmaLinux/EL, Ubuntu |
| [`selinux`](roles/selinux/README.md) | SELinux installation and configuration. | AlmaLinux/EL |
| [`ssh`](roles/ssh/README.md) | SSH installation and configuration. | Debian, AlmaLinux/EL, Ubuntu |
| [`sudo`](roles/sudo/README.md) | SUDO configuration and hardening. | Debian, AlmaLinux/EL, Ubuntu |
| [`sysctl`](roles/sysctl/README.md) | Applies kernel runtime hardening through sysctl: generic kernel, IPv4, and IPv6 network and memory-protection settings, with optional IPv6 disablement. | Debian, AlmaLinux/EL, Ubuntu |
| [`systemdconf`](roles/systemdconf/README.md) | Ansible role to configure systemd system.conf and user.conf files. | Debian, AlmaLinux/EL, Ubuntu |
| [`tcpwrappers`](roles/tcpwrappers/README.md) | tcpwrappers, hosts.allow and hosts.deny, management. | Debian, AlmaLinux/EL, Ubuntu |
| [`timesyncd`](roles/timesyncd/README.md) | Ansible role to manage timesyncd configuration. | Debian, AlmaLinux/EL, Ubuntu |
| [`ufw`](roles/ufw/README.md) | An Ansible role to manage UFW (Uncomplicated Firewall) rules. | Debian, AlmaLinux/EL, Ubuntu |
| [`umask`](roles/umask/README.md) | Configure system-wide default UMASK settings for AlmaLinux, Debian, and Ubuntu via login.defs, shell profiles, and PAM. | Debian, AlmaLinux/EL, Ubuntu |
| [`usbguard`](roles/usbguard/README.md) | Ansible role to manage USBGuard, a software for implementing USB device authorization policies. | Debian, AlmaLinux/EL, Ubuntu |

## Testing

- `ansible-lint` lints against `profile: production` (`.ansible-lint`).
- `molecule test -s docker` converges every role in
  `extensions/molecule/resources/converge.yml` against AlmaLinux, Debian, and
  Ubuntu containers, checks idempotence, and runs the verifiers in
  `extensions/molecule/tests/`.
- `tox -e docker` runs `ansible-lint` followed by `molecule test -s docker`.
- `tox -e devel` and `tox -e upstream` run the same suite against the
  `default` scenario and against unpinned upstream
  `ansible-core`/`ansible-lint`, respectively.
- The `default` scenario (`extensions/molecule/default`) boots the same three
  platforms as genericcloud qcow2 images directly under
  `qemu-system-x86_64`, instead of containers. It requires
  `qemu-system-x86_64`, `qemu-img`, `genisoimage`, and OVMF UEFI firmware
  installed on the host.
- The `prerelease` scenario (`extensions/molecule/prerelease`), run with
  `molecule test -s prerelease` or `tox -e prerelease`, uses the same QEMU
  provisioning and the same converge and verify playbooks, but against the
  current pre-release images: AlmaLinux Kitten 10, Debian 14 `forky` daily,
  and the Ubuntu development release. Those images move, so the scenario
  re-downloads them on every run and is expected to break occasionally. It
  runs weekly, and on demand, from
  `.github/workflows/molecule-prerelease.yml`, which is deliberately not
  triggered by pull requests so that it never gates a merge.

## Security

See [SECURITY.md](SECURITY.md) for the supported-versions policy and
vulnerability reporting.

## License

Apache-2.0. See [LICENSE](LICENSE).
