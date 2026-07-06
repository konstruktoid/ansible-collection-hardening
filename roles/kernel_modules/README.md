# kernel_modules

Kernel module blocklist/blacklist management for AlmaLinux, Debian and Ubuntu.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/kernel_modules/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `fs_modules_blocklist` | `["cramfs", "freevxfs", "hfs", "hfsplus", "jffs2", "squashfs", "udf"]` | Filesystem kernel modules to block and blacklist. |
| `misc_modules_blocklist` | `["algif_aead", "bluetooth", "bnep", "btusb", "can", "cpia2", "esp4", "esp6", "firewire-core", "floppy", "ksmbd", "n_hdlc", "net-pf-31", "pcspkr", "rxrpc", "soundcore", "thunderbolt", "usb-midi", "usb-storage", "uvcvideo", "v4l2_common"]` | Misc kernel modules to block and blacklist. |
| `net_modules_blocklist` | `["atm", "dccp", "sctp", "rds", "tipc"]` | Network kernel modules to block and blacklist. |

## Tasks

`tasks/main.yml` executes, in order:

1. Ensure kmod is installed
2. Write kernel module blacklist configuration
3. Blacklist kernel file system modules
4. Blacklist kernel network modules
5. Gather installed package facts
6. Set fact if usbguard is installed
7. Allow USB-prefixed kernel modules if USBGuard is used
8. Blacklist misc kernel modules
9. Block blacklisted kernel modules

## Handlers

- Rebuild initramfs on Debian
- Rebuild initramfs on RedHat

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.kernel_modules
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
