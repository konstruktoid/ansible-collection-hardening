# prelink

Disable prelink/prelinking on AlmaLinux, Debian, and Ubuntu systems.

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

1. Stat /etc/sysconfig/prelink
2. Stat /etc/prelink.conf
3. Ensure PRELINKING=no in /etc/sysconfig/prelink
4. Get prelink version
5. Run prelink -ua

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.prelink
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
