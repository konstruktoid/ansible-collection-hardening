# file_permissions

Ensure account database and bootloader configuration permissions.

The role restricts the ownership and permissions of the account databases and of
the bootloader configuration files, so that credentials and boot parameters are
not exposed to unprivileged users. Files that do not exist on the target host are
skipped.

Bootloader files are managed when they are readable or writable by group or
other, or when they are not owned by `root:root`. A file that is already
inaccessible to group and other keeps its mode and only has its ownership
corrected: `grub-mkconfig` writes `/boot/grub/grub.cfg` with mode `0400`, and
rewriting it to `file_permissions_bootloader_mode` would both widen the mode and
make the role report a change on every run. Files on the `vfat` EFI system
partition are not managed at all, since that file system has no Unix
permissions.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/file_permissions/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_permissions_account_databases` | See `defaults/main.yml` | The account databases to manage, and the ownership and permissions to apply to them. |
| `file_permissions_bootloader` | `true` | Manage the ownership and permissions of the bootloader configuration files listed in `file_permissions_bootloader_files`. |
| `file_permissions_bootloader_files` | `["/boot/grub/grub.cfg", "/boot/grub/grubenv", "/boot/grub/user.cfg", "/boot/grub2/grub.cfg", "/boot/grub2/grubenv", "/boot/grub2/user.cfg", "/boot/loader/loader.conf"]` | Bootloader configuration files that should be owned by `root:root` and not readable or writable by group or other. |
| `file_permissions_bootloader_mode` | `"0600"` | The file mode applied to a `file_permissions_bootloader_files` entry that is readable or writable by group or other. |
| `file_permissions_opasswd_mode` | `"0600"` | File mode of `/etc/security/opasswd` and `/etc/security/opasswd.old`, the `pam_pwhistory` password history databases. |
| `file_permissions_passwd` | `true` | Manage the ownership and permissions of the `file_permissions_account_databases` files. |
| `file_permissions_passwd_backup_mode` | `"0600"` | File mode of the `/etc/passwd-` and `/etc/group-` backup files. |
| `file_permissions_passwd_mode` | `"0644"` | File mode of the world readable account databases, `/etc/passwd` and `/etc/group`. |
| `file_permissions_shadow_group` | `"shadow"` on the Debian family, `"root"` otherwise | Owner group of `/etc/shadow`, `/etc/shadow-`, `/etc/gshadow` and `/etc/gshadow-`. |
| `file_permissions_shadow_mode` | `"0640"` on the Debian family, `"0000"` otherwise | File mode of `/etc/shadow`, `/etc/shadow-`, `/etc/gshadow` and `/etc/gshadow-`. |

## Tasks

`tasks/main.yml` executes, in order:

1. Configure account database ownership and permissions
2. Stat account databases
3. Set account database ownership and permissions
4. Restrict bootloader configuration permissions
5. Stat bootloader configuration
6. Set bootloader configuration ownership and permissions

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.file_permissions
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `permissions`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
