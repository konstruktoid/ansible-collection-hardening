# sysctl

Applies kernel runtime hardening through sysctl: generic kernel, IPv4, and IPv6 network and memory-protection settings, with optional IPv6 disablement.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | resolute |

## Role variables

Defined in `roles/sysctl/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `disable_ipv6` | `false` | If True, disable IPv6 on the system. |
| `generic_sysctl_settings` | mapping, see below | Generic sysctl settings. |
| `ipv4_sysctl_settings` | mapping, see below | IPv4 sysctl settings. |
| `ipv6_disable_sysctl_settings` | mapping, see below | IPv6 sysctl settings to disable IPv6. |
| `ipv6_sysctl_settings` | mapping, see below | IPv6 sysctl settings. |
| `sysctl_ipv6_config_template` | `"etc/sysctl/sysctl.ipv6.conf.j2"` | IPv6 sysctl configuration template location. |
| `sysctl_main_config_template` | `"etc/sysctl/sysctl.main.conf.j2"` | main sysctl configuration template location. |
| `sysctl_net_ipv6_conf_accept_ra_rtr_pref` | `0` | If 0, the system denies IPv6 router solicitations. |
| `sysctl_conf_dir` | `""` | Sets the sysctl configuration directory. A value set here is honoured as-is, and is not overwritten by detection. If empty, the directory is `/usr/lib/sysctl.d` when `usr_lib_sysctl_d_dir` is True or when `/usr/lib/sysctl.d` exists, otherwise `/etc/sysctl.d`. |
| `usr_lib_sysctl_d_dir` | `false` | If True, use `/usr/lib/sysctl.d` as the sysctl configuration directory. If False, the directory is detected. Ignored if `sysctl_conf_dir` is set. |
| `sysctl_dev_tty_ldisc_autoload` | `0` | If 0, restrict loading TTY line disciplines to the CAP_SYS_MODULE capability. |

`generic_sysctl_settings` default value:

```yaml
fs.protected_fifos: 2
fs.protected_regular: 2
fs.protected_hardlinks: 1
fs.protected_symlinks: 1
fs.suid_dumpable: 0
kernel.core_pattern: '|/bin/false'
kernel.core_uses_pid: 1
kernel.dmesg_restrict: 1
kernel.kptr_restrict: 2
kernel.panic: 60
kernel.panic_on_oops: 1
kernel.perf_event_paranoid: 2
kernel.randomize_va_space: 2
kernel.sysrq: 0
kernel.unprivileged_bpf_disabled: 1
kernel.unprivileged_userns_clone: 0
kernel.yama.ptrace_scope: 2
net.core.bpf_jit_harden: 2
user.max_user_namespaces: 0
```

`ipv4_sysctl_settings` default value:

```yaml
net.ipv4.conf.all.accept_redirects: 0
net.ipv4.conf.all.accept_source_route: 0
net.ipv4.conf.all.log_martians: 1
net.ipv4.conf.all.rp_filter: 1
net.ipv4.conf.all.secure_redirects: 1
net.ipv4.conf.all.send_redirects: 0
net.ipv4.conf.all.shared_media: 1
net.ipv4.conf.default.accept_redirects: 0
net.ipv4.conf.default.accept_source_route: 0
net.ipv4.conf.default.log_martians: 1
net.ipv4.conf.default.rp_filter: 1
net.ipv4.conf.default.secure_redirects: 1
net.ipv4.conf.default.send_redirects: 0
net.ipv4.conf.default.shared_media: 1
net.ipv4.icmp_echo_ignore_broadcasts: 1
net.ipv4.icmp_ignore_bogus_error_responses: 1
net.ipv4.ip_forward: 0
net.ipv4.tcp_challenge_ack_limit: 2147483647
net.ipv4.tcp_invalid_ratelimit: 500
net.ipv4.tcp_max_syn_backlog: 20480
net.ipv4.tcp_rfc1337: 1
net.ipv4.tcp_syn_retries: 5
net.ipv4.tcp_synack_retries: 5
net.ipv4.tcp_syncookies: 1
net.ipv4.tcp_timestamps: 1
```

`ipv6_disable_sysctl_settings` default value:

```yaml
net.ipv6.conf.all.disable_ipv6: 1
net.ipv6.conf.default.disable_ipv6: 1
```

`ipv6_sysctl_settings` default value:

```yaml
net.ipv6.conf.all.accept_ra: 0
net.ipv6.conf.all.accept_redirects: 0
net.ipv6.conf.all.accept_source_route: 0
net.ipv6.conf.all.forwarding: 0
net.ipv6.conf.all.use_tempaddr: 2
net.ipv6.conf.default.accept_ra: 0
net.ipv6.conf.default.accept_ra_defrtr: 0
net.ipv6.conf.default.accept_ra_pinfo: 0
net.ipv6.conf.default.accept_ra_rtr_pref: 0
net.ipv6.conf.default.accept_redirects: 0
net.ipv6.conf.default.accept_source_route: 0
net.ipv6.conf.default.autoconf: 0
net.ipv6.conf.default.dad_transmits: 0
net.ipv6.conf.default.max_addresses: 1
net.ipv6.conf.default.router_solicitations: 0
net.ipv6.conf.default.use_tempaddr: 2
```

## Tasks

`tasks/main.yml` executes, in order:

1. Resolve the sysctl configuration directory
2. Stat IPv6 status
3. Set IPv6 fact
4. Ensure sysctl configuration dir has the correct permissions
5. Template the sysctl file with general sysctl hardening settings
6. Template sysctl file with IPv6 settings

## Handlers

- Restart sysctl

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.sysctl
```

## Tags

`almalinux`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
