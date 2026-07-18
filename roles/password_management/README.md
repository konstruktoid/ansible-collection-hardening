# password_management

Configures PAM (`common-auth`, `common-account`, `common-password`, `faillock`, `pwquality`) and system-wide crypto-policies to enforce password quality requirements, hashing algorithm, account lockout, and FIPS mode.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/password_management/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `common_account_template` | `"etc/pam.d/common-account.j2"` | PAM common-account template location. |
| `common_auth_template` | `"etc/pam.d/common-auth.j2"` | PAM common-auth template location. |
| `common_password_template` | `"etc/pam.d/common-password.j2"` | PAM common-password template location. |
| `manage_faillock` | `true` | If True, enable and manage faillock. |
| `faillock` | mapping, see below | Faillock configuration options. |
| `faillock_conf_template` | `"etc/security/faillock.conf.j2"` | faillock.conf template location. |
| `manage_pwquality` | `true` | If True, enable and manage pwquality. |
| `pwquality` | mapping, see below | pwquality configuration options. |
| `pwquality_conf_template` | `"etc/security/pwquality.conf.j2"` | pwquality.conf template location. |
| `login_template` | `"etc/pam.d/login.j2"` | login template location |
| `set_crypto_policy` | `true` | Set and use cryptographic policies if `/etc/crypto-policies/config` exists and `set_crypto_policy: true`. |
| `crypto_policy` | `"DEFAULT"` | The cryptographic policy to set if `set_crypto_policy: true`. |
| `manage_pam` | `true` | If True, manage PAM configuration files. |
| `password_remember` | `24` | The number of previous passwords to remember and not allow the user to reuse. |

`faillock` default value:

```yaml
admin_group: ''
audit: true
deny: 5
dir: /var/run/faillock
even_deny_root: true
fail_interval: 900
local_users_only: true
no_log_info: false
nodelay: true
root_unlock_time: 600
silent: false
unlock_time: 600
```

`pwquality` default value:

```yaml
dcredit: -1
dictcheck: true
dictpath: ''
difok: 8
enforce_for_root: true
enforcing: true
gecoscheck: true
lcredit: -1
local_users_only: true
maxclassrepeat: 4
maxrepeat: 3
maxsequence: 3
minclass: 4
minlen: 15
ocredit: -1
retry: 3
ucredit: -1
usercheck: true
usersubstr: 3
```

## Tasks

`tasks/main.yml` executes, in order:

1. Set crypto-policies config as fact
2. Stat crypto-policies config
3. Set config fact
4. Get PAM version
5. Gather package facts
6. Get libpam version in Debian family
7. Get libpam version in RedHat family
8. Set hashing algorithm for password (yescrypt|sha512)
9. Update current facts
10. Configure faillock.conf
11. Debian OS family PAM configuration
12. Configure common-password
13. Configure common-auth
14. Configure common-account
15. Configure login
16. RedHat OS family PAM configuration
17. Check RedHat PAM files for nullok removal
18. Remove 'nullok'
19. Set hashing algorithm for password
20. Set rounds
21. Install and configure pwquality
22. Install pwquality
23. Configure pwquality
24. Stat libuser configuration
25. Set libuser crypt_style
26. Set crypto policy
27. Get crypto-policies value
28. Update crypto-policies
29. Set FIPS mode
30. Add cracklib password list
31. Add local information to password list
32. Get all local user accounts
33. Add local usernames to password list

## Handlers

- Update Debian cracklib
- Update RedHat cracklib

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.password_management
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
