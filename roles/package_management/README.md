# package_management

Role to manage configuration of APT and DNF.

Apply any role that adds a package repository before this one when `system_upgrade` is
enabled. `timesyncd` installs `epel-release` on the RedHat family, for example. A
repository added after the upgrade has run leaves its packages upgradable, so the next
run of this role reports changed again.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/package_management/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `apt_options` | `['Acquire::AllowDowngradeToInsecureRepositories "0";', 'Acquire::AllowInsecureRepositories "0";', 'Acquire::AllowWeakRepositories "0";', 'Acquire::Check-Date "true";', 'Acquire::http::AllowRedirect "false";', 'APT::Get::AllowUnauthenticated "false";', 'APT::Get::AutomaticRemove "true";', 'APT::Install-Recommends "0";', 'APT::Install-Suggests "0";', 'APT::Periodic::AutocleanInterval "7";', 'APT::Sandbox::Seccomp "1";', 'Unattended-Upgrade::Remove-Unused-Dependencies "true";', 'Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";']` | Options used to configure the APT suite of tools. |
| `apt_seccomp_broken_releases` | `['forky', 'trixie']` | Debian releases where APT's seccomp sandbox aborts the acquire methods, `E:Method file has died unexpectedly!`, and where `APT::Sandbox::Seccomp` therefore has to be left off. |
| `system_upgrade` | `true` | If True, then the installed packages will be upgraded to the latest version using `apt` or `dnf`. |

## Tasks

`tasks/main.yml` executes, in order:

1. Apt configuration and upgrades
2. Configure APT
3. Remove APT seccomp sandboxing on affected Debian releases
4. Run apt upgrade
5. Dnf configuration
6. Set yum.conf gpgcheck
7. Set yum.conf clean_requirements
8. Set yum.conf localpkg_gpgcheck
9. Set yum.conf repo_gpgcheck
10. Enable dnf repositories and upgrades
11. Stat PowerTools repository files
12. Enable the PowerTools repository
13. Update dnf cache
14. Run dnf upgrade

## Handlers

- Run apt-get autoremove
- Run apt-get clean
- Run dnf autoremove

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.package_management
```

## Tags

`almalinux`, `apt`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `ubuntu`, `yum`

## License

Apache-2.0
