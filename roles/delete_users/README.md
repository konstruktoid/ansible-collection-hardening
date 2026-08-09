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

## Notes

On the Debian family the default accounts are owned by the packaging system, and two independent
package hooks recreate them after this role has removed them:

- `systemd` ships `/usr/lib/sysusers.d/basic.conf`, generated from `base-passwd`'s `passwd.master`,
  and `dh_installsysusers` adds `systemd-sysusers basic.conf ...` to `systemd.postinst`. Every
  install or upgrade of the `systemd` package therefore recreates `games`, `irc`, `list`, `news`,
  `sync` and `uucp`. The postinst snippet a package gets from `dh_installsysusers` only processes
  the `sysusers.d` files that package itself declares and installs, not everything in
  `/usr/lib/sysusers.d/`, so these accounts return when `systemd`, or any other package shipping
  and processing `basic.conf`, is installed or upgraded.
- `base-passwd.postinst` runs `update-passwd` on every *upgrade* of `base-passwd`. When debconf is
  available, which it is on a normal system, it runs unprompted and recreates every account listed
  in `passwd.master`.

Two consequences:

- Run this role **after** every role or task that installs or upgrades packages. Placing it early
  in a play that later installs or upgrades `systemd`, for example through
  `konstruktoid.hardening.resolvedconf` pulling a `systemd` install or upgrade into the same
  transaction as `systemd-resolved`, leaves the accounts present at the end of the run and makes
  the play non-idempotent. Installing `systemd-resolved` on its own only creates the
  `systemd-resolve` user, since its postinst processes `systemd-resolve.conf` and not `basic.conf`.
- Even with correct ordering the removal is not permanent. A later `systemd` or `base-passwd`
  upgrade, including one applied by unattended upgrades, brings the accounts back. Re-run the role
  periodically if their absence has to hold over time.

The `sysusers.d` path can be suppressed with a filtered copy of `basic.conf` in `/etc/sysusers.d/`,
which takes precedence over the one in `/usr/lib/sysusers.d/`. This role does not do that, because
the override masks the vendor file wholesale and would also hide accounts added to it by future
package updates, and because it does not stop the `update-passwd` path.

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
