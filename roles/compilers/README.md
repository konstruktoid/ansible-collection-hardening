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

1. Find available compilers
2. Resolve compiler matches to the files they point to
3. Stat resolved compilers
4. Set the list of compiler files to restrict
5. Restrict compilers access
6. Check dpkg-statoverride for restricted compilers access
7. Ensure restrict compilers access via dpkg-statoverride
8. Ensure DNF post-transaction-actions plugin is installed
9. Ensure DNF post-transaction-actions plugin directory exists
10. Ensure restrict compilers access via DNF post-transaction-actions Plugin

## Symlinks

Names that match `compilers` are often symlinks, for example `/usr/bin/gcc` and `/usr/bin/cc`
on Debian and Ubuntu. The role resolves each match to the regular file it points to, removes
duplicates (for example `/bin/make` and `/usr/bin/make` on merged-`/usr` systems) and sets mode
`0750` on that file. On Debian and Ubuntu the `dpkg-statoverride` entry and on AlmaLinux the DNF
post-transaction action are recorded against the same file, so a package upgrade restores the
restriction instead of the packaged mode.

Symlinks in `/snap/bin` are skipped, as they point to the shared `snap` binary. Because the
target is restricted, a name in `compilers` that links to a multi-call binary, such as
`/usr/local/bin/gcc` pointing to `ccache`, restricts that binary for non-root users.

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
