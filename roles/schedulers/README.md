# schedulers

Configure scheduled command services.

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

## Tasks

`tasks/main.yml` executes, in order:

1. Configure scheduled command services
2. Gather service facts
3. Remove cron.deny and at.deny
4. Check whether cron and at allow files exist
5. Clean cron and at
6. Allow root cron and at
7. Mask atd
8. Set cron permissions
9. Check whether /etc/crontab exists
10. Set crontab permissions

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.schedulers
```

## Tags

`almalinux`, `atd`, `cis`, `cron`, `debian`, `disa`, `hardening`, `security`, `system`, `ubuntu`

## License

Apache-2.0
