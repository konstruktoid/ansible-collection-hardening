# package_management

Role to manage configuration of APT and DNF.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/package_management/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `apt_options` | `['Acquire::AllowDowngradeToInsecureRepositories "false";', 'Acquire::AllowInsecureRepositories "false";', 'Acquire::http::AllowRedirect "false";', 'APT::Get::AllowUnauthenticated "false";', 'APT::Get::AutomaticRemove "true";', 'APT::Install-Recommends "false";', 'APT::Install-Suggests "false";', 'APT::Periodic::AutocleanInterval "7";', 'APT::Sandbox::Seccomp "1";', 'Unattended-Upgrade::Remove-Unused-Dependencies "true";', 'Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";']` | Options used to configure the APT suite of tools. |
| `system_upgrade` | `true` | If True, then the installed packages will be upgraded to the latest version using `apt` or `dnf`. |

## Tasks

`tasks/main.yml` executes, in order:

1. Apt configuration and upgrades
2. Configure APT
3. Run apt upgrade
4. Dnf configuration
5. Link dnf.conf
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

`almalinux`, `apt`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `ubuntu`, `yum`

## License

Apache-2.0
