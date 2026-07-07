# apport

Manage Apport.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/apport/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `disable_apport` | `true` | If true, disable and mask the Apport crash-reporting service. |

## Tasks

`tasks/main.yml` executes, in order:

1. Disable apport

## Handlers

- Mask apport

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.apport
```

## Tags

`apport`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
