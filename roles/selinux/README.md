# selinux

SELinux installation and configuration.

## Requirements

- Ansible-core >= 2.18
- `ansible.posix` >= 2.2.0

## Supported platforms

| Platform | Versions |
| --- | --- |
| AlmaLinux / EL | 10 |

## Role variables

Defined in `roles/selinux/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `selinux_install_packages` | `true` | If True, install SELinux userspace utilities and the targeted policy. |
| `selinux_packages` | list, see below | SELinux packages to install. |
| `selinux_packages_blocklist` | list, see below | Packages to remove, as they increase attack surface and are not required on a hardened, non-interactive host. |
| `selinux_policy` | `"targeted"` | The SELinux policy to use. |
| `selinux_state` | `"enforcing"` | The SELinux mode. One of `enforcing`, `permissive` or `disabled`. |
| `selinux_update_kernel_param` | `true` | If True, also remove the `selinux=0` kernel command line argument using grubby. |

`selinux_packages` default value:

```yaml
libselinux-utils
policycoreutils
policycoreutils-python-utils
python3-libselinux
selinux-policy-targeted
```

`selinux_packages_blocklist` default value:

```yaml
mcstrans
setroubleshoot
setroubleshoot-server
```

## Tasks

`tasks/main.yml` executes, in order, on AlmaLinux/EL hosts:

1. Install SELinux packages
2. Remove SELinux related packages
3. Configure SELinux state and policy
4. Remove enforcing=0 from the kernel command line
5. Notify if a reboot is required for the SELinux state to take effect

The state, policy, and kernel-command-line steps are skipped inside
containers, since a container's kernel is shared with the host and
`setenforce`/grubby changes there are either unavailable or meaningless.
Package installation and removal still run in containers.

Changing `selinux_state` to or from `disabled` requires a reboot before it
takes effect; the role will not reboot the host itself, matching how the
`kernel` and `apparmor` roles handle GRUB-only changes.

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.selinux
```

## Tags

`almalinux`, `cis`, `disa`, `hardening`, `security`, `selinux`, `system`, `systemd`

## License

Apache-2.0
