# delete_users

Delete listed users.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/delete_users/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `delete_users` | `["games", "gnats", "irc", "list", "news", "sync", "uucp"]` | List of users to delete. |

## Tasks

`tasks/main.yml` executes, in order:

1. Remove users

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.delete_users
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
