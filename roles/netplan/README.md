# netplan

Ensure netplan configuration permissions.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

This role has no configurable variables.

## Operational notes

Netplan-generated files in `/run/systemd/network` are runtime state and are
not managed by this role. When the `sudo` and `umask` roles are both applied
where `/usr/sbin/netplan` is installed, the `sudo` role uses a
Netplan-specific `0027` umask so generated `root:systemd-network` files
remain readable by `systemd-networkd` without weakening the system-wide umask.

## Tasks

`tasks/main.yml` executes, in order:

1. Find and set permissions of netplan configuration files
2. Check if netplan directories exist
3. Set netplan existing directories
4. Find all netplan configuration files
5. Set permissions of netplan configuration files

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.netplan
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `netplan`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
