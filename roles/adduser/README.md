# adduser

Configure adduser and useradd.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/adduser/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `adduser_conf_template` | `"etc/adduser.conf.j2"` | adduser.conf template location. |
| `useradd_template` | `"etc/default/useradd.j2"` | useradd template location. |

## Tasks

`tasks/main.yml` executes, in order:

1. Add configuration file for adduser and addgroup
2. Add configuration file for useradd

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.adduser
```

## Tags

`adduser`, `almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `ubuntu`, `useradd`

## License

Apache-2.0
