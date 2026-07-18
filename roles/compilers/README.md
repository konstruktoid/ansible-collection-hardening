# compilers

Restrict compiler binaries to root on AlmaLinux, Debian, and Ubuntu systems.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/compilers/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `compilers` | `["as", "cargo", "cc", "cc-[0-9]*", "clang-[0-9]*", "gcc", "gcc-[0-9]*", "go", "make", "rustc"]` | Compilers to restrict to the root user. |

## Tasks

`tasks/main.yml` executes, in order:

1. Stat available compilers
2. Restrict compilers access
3. Check dpkg-statoverride for restricted compilers access
4. Ensure restrict compilers access via dpkg-statoverride
5. Ensure DNF post-transaction-actions plugin is installed
6. Ensure DNF post-transaction-actions plugin directory exists
7. Ensure restrict compilers access via DNF post-transaction-actions Plugin

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.compilers
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
