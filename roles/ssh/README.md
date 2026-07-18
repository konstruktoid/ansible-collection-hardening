# ssh

SSH installation and configuration.

## Requirements

- Ansible-core >= 2.18
- `community.crypto` collection
- `community.general` collection

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/ssh/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `ssh_config_template` | `"etc/ssh/ssh_config.j2"` | OpenSSH ssh_config template location. |
| `sshd_accept_env` | `"LANG LC_*"` | Specifies what environment variables sent by the client will be copied into the session. |
| `sshd_admin_net` | `["192.168.0.0/24", "192.168.1.0/24"]` | Only the network(s) defined in `sshd_admin_net` are allowed to connect to `sshd_ports`. |
| `sshd_allow_agent_forwarding` | `false` | Specifies whether ssh-agent forwarding is permitted. |
| `sshd_allow_groups` | `["sudo"]` | If specified, login is allowed only for users whose primary group or supplementary group list matches one of the patterns. |
| `sshd_allow_tcp_forwarding` | `false` | Specifies whether TCP forwarding is permitted. |
| `sshd_allow_users` | `[]` | If specified, login is allowed only for users whose user name matches one of the patterns. |
| `sshd_authentication_methods` | `"any"` | The authentication methods that must be successfully completed in order to grant access to a user. |
| `sshd_authorized_principals_file` | `"/etc/ssh/auth_principals/%u"` | Specifies a file that lists principal names that are accepted for certificate authentication. |
| `sshd_banner` | `"/etc/issue.net"` | The contents of the specified file are sent to the remote user before authentication. |
| `sshd_ca_signature_algorithms` | `["ecdsa-sha2-nistp384", "ecdsa-sha2-nistp521", "ssh-ed25519", "rsa-sha2-512"]` | Specifies which algorithms are allowed for signing of certificates by certificate authorities. |
| `sshd_ciphers` | `["chacha20-poly1305@openssh.com", "aes256-gcm@openssh.com", "aes256-ctr"]` | Specifies the ciphers allowed. Multiple ciphers must be comma-separated. |
| `sshd_client_alive_count_max` | `1` | Sets the number of client alive messages which may be sent without sshd receiving any messages back from the client. |
| `sshd_client_alive_interval` | `200` | Sets a timeout interval in seconds after which if no data has been received from the client, sshd will send a message requesting a response from the client. |
| `sshd_compression` | `false` | Specifies whether compression is enabled. |
| `sshd_config_d_force_clear` | `false` | Clear pre-existing custom configurations in /etc/ssh/sshd_config.d |
| `sshd_config_force_replace` | `false` | Force replace configuration file `/etc/ssh/sshd_config`. |
| `sshd_config_template` | `"etc/ssh/sshd_config.j2"` | OpenSSH sshd_config template location. |
| `sshd_debian_banner` | `false` | Specifies whether the distribution-specified extra version suffix is included during initial protocol handshake. |
| `sshd_deny_groups` | `[]` | Login is disallowed for users whose primary group or supplementary group list matches one of the patterns. |
| `sshd_deny_users` | `[]` | Login is disallowed for users whose user name matches one of the patterns. |
| `sshd_gateway_ports` | `false` | Specifies whether remote hosts are allowed to connect to ports forwarded for the client. |
| `sshd_gssapi_authentication` | `false` | Specifies whether user authentication based on GSSAPI is allowed. |
| `sshd_host_key_algorithms` | `["ssh-ed25519-cert-v01@openssh.com", "rsa-sha2-512-cert-v01@openssh.com", "ssh-ed25519", "ecdsa-sha2-nistp521-cert-v01@openssh.com", "ecdsa-sha2-nistp384-cert-v01@openssh.com", "ecdsa-sha2-nistp521", "ecdsa-sha2-nistp384"]` | Specifies the host key algorithms that the server offers. |
| `sshd_host_keys_files` | `[]` | Specifies a file containing a private host key used by SSH. If empty `RSA`, `ECDSA`, and `ED25519` will be used, if supported by the installed sshd version. |
| `sshd_host_keys_group` | `"root"` | Owner group of the host keys. |
| `sshd_host_keys_mode` | `"0600"` | Host keys file mode. |
| `sshd_host_keys_owner` | `"root"` | Owner of the host keys. |
| `sshd_hostbased_authentication` | `false` | Specifies whether rhosts or /etc/hosts.equiv authentication together with successful public key client host authentication is allowed. |
| `sshd_ignore_rhosts` | `true` | Specifies that .rhosts and .shosts files will not be used in HostbasedAuthentication. |
| `sshd_ignore_user_known_hosts` | `true` | Specifies whether sshd should ignore the user's ~/.ssh/known_hosts during HostbasedAuthentication and use only the system-wide known hosts file /etc/ssh/known_hosts. |
| `sshd_kbd_interactive_authentication` | `false` | Specifies whether to allow keyboard-interactive authentication. |
| `sshd_kerberos_authentication` | `false` | Specifies whether the password provided by the user for PasswordAuthentication will be validated through the Kerberos KDC. |
| `sshd_kex_algorithms` | `["mlkem768x25519-sha256", "sntrup761x25519-sha512", "curve25519-sha256", "curve25519-sha256@libssh.org", "ecdh-sha2-nistp521", "ecdh-sha2-nistp384"]` | Specifies the available KEX (Key Exchange) algorithms. |
| `sshd_listen` | `["0.0.0.0"]` | Specifies the addresses sshd should listen on. |
| `sshd_log_level` | `"verbose"` | Gives the verbosity level that is used when logging messages from sshd. |
| `sshd_login_grace_time` | `20` | The server disconnects after this time if the user has not successfully logged in. |
| `sshd_macs` | `["hmac-sha2-512-etm@openssh.com", "hmac-sha2-256-etm@openssh.com", "hmac-sha2-512", "hmac-sha2-256"]` | Specifies the available MAC (Message Authentication Code) algorithms. |
| `sshd_match_addresses` | `[]` | Add a conditional block for addresses. |
| `sshd_match_groups` | `[]` | Add a conditional block for groups. |
| `sshd_match_local_ports` | `[]` | Add a conditional block for ports. |
| `sshd_match_users` | `[]` | Add a conditional block for users. |
| `sshd_max_auth_tries` | `3` | Specifies the maximum number of authentication attempts permitted per connection. |
| `sshd_max_sessions` | `3` | Specifies the maximum number of open sessions permitted per network connection. |
| `sshd_max_startups` | `"10:30:60"` | Specifies the maximum number of concurrent unauthenticated connections to the SSH daemon. |
| `sshd_password_authentication` | `false` | Specifies whether password authentication is allowed. |
| `sshd_permit_empty_passwords` | `false` | Specifies whether the server allows login to accounts with empty password strings. |
| `sshd_permit_root_login` | `false` | Specifies whether root can log in using ssh, if True then the option is set to prohibit-password. |
| `sshd_permit_tunnel` | `false` | Specifies whether tun device forwarding is allowed. |
| `sshd_permit_user_environment` | `false` | Specifies whether user environment variables are processed by sshd. |
| `sshd_ports` | `[22]` | Specifies the port number that sshd listens on. |
| `sshd_print_last_log` | `true` | Specifies whether sshd should print the last user login when a user logs in interactively. |
| `sshd_print_motd` | `false` | Specifies whether sshd should print /etc/motd when a user logs in interactively. |
| `sshd_print_pam_motd` | `false` | Specifies whether pam_motd should be enabled for sshd. |
| `sshd_rekey_limit` | `"512M 1h"` | Specifies the maximum amount of data that may be transmitted before the session key is renegotiated. |
| `sshd_required_ecdsa_size` | `521` | Required ECDSA key size when generating new host keys. |
| `sshd_required_rsa_size` | `4096` | Required RSA key size when generating new host keys. |
| `sshd_sftp_chroot` | `true` | Specifies whether the SFTP subsystem should chroot users. |
| `sshd_sftp_chroot_dir` | `"%h"` | Specifies the pathname of a directory to chroot to after authentication. |
| `sshd_sftp_enabled` | `true` | Specifies whether the SFTP subsystem should be enabled. |
| `sshd_sftp_only_group` | `""` | Specifies the name of the group that will have access restricted to the sftp service only. |
| `sshd_sftp_subsystem` | `"internal-sftp -f LOCAL6 -l INFO"` | Specifies the SFTP subsystem to use. |
| `sshd_strict_modes` | `true` | Specifies whether sshd should check file modes and ownership of the user's files and home directory before accepting login. |
| `sshd_syslog_facility` | `"auth"` | Gives the facility code that is used when logging messages from sshd. |
| `sshd_tcp_keep_alive` | `false` | Specifies whether the system should send TCP keepalive messages to the other side. |
| `sshd_tmpfiles_template` | `"usr/lib/tmpfiles.d/ssh.conf.j2"` | OpenSSH tmpfiles template location. |
| `sshd_trusted_user_ca_keys_base64` | `""` | Public keys of trusted certificate authoritites in base64 format. |
| `sshd_trusted_user_ca_keys_file` | `"/etc/ssh/trusted-user-ca-keys.pem"` | Specifies a file containing public keys of certificate authorities that are trusted to sign user certificates for authentication. |
| `sshd_update_moduli` | `false` | Specifies whether the moduli file should be updated. |
| `sshd_update_moduli_url` | `"https://raw.githubusercontent.com/konstruktoid/ssh-moduli/main/moduli"` | Specifies the URL to download the moduli file from. |
| `sshd_use_dns` | `false` | Specifies whether sshd should look up the remote host name, and to check that the resolved host name for the remote IP address maps back to the very same IP address. |
| `sshd_use_pam` | `true` | If true, this will enable PAM authentication. |
| `sshd_use_privilege_separation` | `"sandbox"` | Specifies whether sshd separates privileges by creating an unprivileged child process to deal with incoming network traffic. |
| `sshd_x11_forwarding` | `false` | Specifies whether X11 forwarding is permitted. |
| `use_crypto_policies` | `true` | If true, the role will use the system's crypto policy to determine which algorithms to use for ssh and sshd configuration. |

## Tasks

`tasks/main.yml` executes, in order:

1. Install OpenSSH server package
2. Get installed sshd version
3. Set ssh version as fact
4. Print SSH version fact
5. Ensure privilege separation directories exist
6. Configure sshd using sshd_config.d
7. Stat sysconfig sshd configuration
8. Remove sshd system crypto policy
9. Get sshd Include config
10. Check if sshd_config.d exists
11. Clear pre-existing custom configurations in /etc/ssh/sshd_config.d
12. Search pre-existing custom configurations in /etc/ssh/sshd_config.d
13. Clear pre-existing custom configurations in /etc/ssh/sshd_config.d
14. Ensure /etc/ssh/sshd_config permissions
15. SSH moduli file
16. Stat moduli file
17. Update moduli file
18. Find DSA host files
19. Remove DSA host files
20. Set default for sshd_host_keys_files if not supplied
21. Generate SSH RSA keypair
22. Generate SSH ECDSA keypair
23. Generate SSH Ed25519 keypair
24. Set hostkeys according to openssh-version if openssh >= 5.3
25. Set hostkeys according to openssh-version if openssh >= 6.0
26. Set hostkeys according to openssh-version if openssh >= 6.5
27. Disable PAM dynamic MOTD
28. Check variable sshd_config_force_replace
29. Create trusted ca keys
30. Configure sshd
31. Configure sshd using sshd_config.d
32. Remove possible Subsystem duplicate
33. Stat sshd host keys
34. Set sshd host key permissions
35. Configure ssh
36. Check if ssh_config.d exists
37. Configure ssh client

## Handlers

- Restart ssh socket
- Restart ssh service
- Disable ssh service

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.ssh
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `ssh`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
