# lock_root

Lock the root account and remove root SSH authorized_keys.

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

1. Lock the root account and remove ssh authorized keys
2. Lock the root account
3. Remove ssh authorized keys for root
4. Check that root ssh authorized keys are absent
5. Assert root ssh authorized keys are absent

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.lock_root
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
