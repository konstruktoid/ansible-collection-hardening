# umask

Configure system-wide default UMASK settings for AlmaLinux, Debian, and Ubuntu via login.defs, shell profiles, and PAM.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/umask/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `umask_value` | `"0077"` | Sets the default umask value. |

## Tasks

`tasks/main.yml` executes, in order:

1. Set UMASK in login.defs if it exists else add it
2. Stat init.d/rc
3. Set default rc umask
4. Ensure that a umask line appears in rc
5. Stat bashrc
6. Ensure that a umask line appears in bashrc
7. Stat bash.bashrc
8. Ensure that a umask line appears in bash.bashrc
9. Stat csh.cshrc
10. Ensure that a umask line appears in csh.cshrc
11. Ensure that a umask line appears in profile
12. Stat /etc/profile.d
13. Find all files in /etc/profile.d
14. Set default profile umask for each file in /etc/profile.d
15. Find PAM files containing pam_umask.so
16. Ensure pam_umask has the desired umask

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.umask
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
