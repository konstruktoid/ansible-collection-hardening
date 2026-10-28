# kernel_modules

Kernel module blocklist/blacklist management for AlmaLinux, Debian and Ubuntu.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/kernel_modules/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `fs_modules_blocklist` | `["cramfs", "freevxfs", "hfs", "hfsplus", "jffs2", "squashfs", "udf"]` | Filesystem kernel modules to block and blacklist. |
| `misc_modules_blocklist` | `["act_pedit", "ah4", "ah6", "algif_aead", "bluetooth", "bnep", "btusb", "can", "cpia2", "esp4", "esp6", "firewire-core", "floppy", "ksmbd", "n_hdlc", "net-pf-31", "nlmon", "pcspkr", "rxrpc", "soundcore", "thunderbolt", "usb-midi", "usb-storage", "uvcvideo", "v4l2_common"]` | Misc kernel modules to block and blacklist. |
| `net_modules_blocklist` | `["atm", "dccp", "pppoe", "sctp", "rds", "tipc"]` | Network kernel modules to block and blacklist. |

## Notes

Every listed module is both blacklisted and blocked, so the feature it provides is unavailable on
the host. Among the defaults, `act_pedit` disables `tc` packet-editing actions, `ah4`, `ah6`, `esp4`
and `esp6` disable IPsec, `nlmon` disables netlink monitoring interfaces, and `pppoe` disables PPP
over Ethernet. `act_pedit` and `nlmon` are blocked because the public ZDI-CAN-33367 root exploit
depends on them; `ah6` and `pppoe` because of CVE-2026-80844 (DirtyAH6) and CVE-2026-68121
(PPPoEject).

To keep a module available, set the list that contains it to a complete list that omits it.
Lists replace the defaults rather than merging with them.

On a host where the role has already run, omitting a module is not enough on its own. The
`blacklist` files in `/etc/modprobe.d/` are rewritten from the current lists. The
`install <module> /bin/true` lines in `/etc/modprobe.d/blacklist-blocked.conf` are only ever added,
never removed, so remove the module's line from that file by hand. Then rebuild the initramfs
(`update-initramfs -u` on Debian and Ubuntu, `dracut -f` on AlmaLinux) before the module can load
again.

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

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
