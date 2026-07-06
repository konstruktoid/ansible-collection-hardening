# ctrlaltdel

Disable Ctrl+Alt+Del key sequence to prevent reboots.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

This role has no configurable variables.

## Tasks

`tasks/main.yml` executes, in order:

1. Mask ctrl-alt-del
2. Mask ctrl-alt-del via symlink
3. Reload systemd
4. Mask ctrl-alt-del via systemd

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.ctrlaltdel
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
