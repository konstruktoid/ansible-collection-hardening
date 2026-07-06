# mount

Manage /dev/shm, /proc and /tmp mounts.

## Requirements

- Ansible-core >= 2.18
- `ansible.posix` collection

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/mount/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `hide_pid` | `2` | This option controls who can access the information in `/proc/pid` directories |
| `process_group` | `0` | Specifies the GID of the group that can access (/proc/pid) directories when `hide_pid` is set to 2. |
| `tmp_mount_template` | `"etc/systemd/system/tmp.mount.j2"` | tmp.mount template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Mount /proc with additional options
2. Stat /dev/shm
3. Mount /dev/shm with noexec
4. Configure /tmp mount
5. Add systemd tmp.mount
6. Stat tmp.mount
7. Unmask and start tmp.mount
8. Remove /tmp from fstab
9. Unmask tmp.mount
10. Start tmp.mount

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.mount
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
