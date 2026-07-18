# disable_wireless

Disable wireless interfaces and wireless kernel modules on AlmaLinux, Debian, and Ubuntu systems.

## Requirements

- Ansible-core >= 2.18
- `community.general` collection

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

This role has no configurable variables.

## Tasks

`tasks/main.yml` executes, in order:

1. Disable wireless interfaces
2. Ensure nmcli is available
3. Turn off and disable wireless interfaces
4. Check Wi-Fi radio state
5. Check WWAN radio state
6. Turn off wireless interfaces
7. Get kernel modules
8. Disable wireless kernel modules

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.disable_wireless
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
