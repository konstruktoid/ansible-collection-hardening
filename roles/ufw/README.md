# ufw

An Ansible role to manage UFW (Uncomplicated Firewall) rules.

## Requirements

- Ansible-core >= 2.18
- `ansible.posix` collection
- `community.general` collection

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/ufw/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `conntrack_sysctl_settings` | mapping, see below | Netfilter connection tracking sysctl settings. |
| `disable_ipv6` | `false` | If True, IPv6 support is disabled. |
| `ufw_admin_net` | `["192.168.0.0/24", "192.168.1.0/24"]` | Only the network(s) defined in `ufw_admin_net` are allowed to connect to `ufw_ports`. |
| `ufw_ports` | `[22]` | Specifies the port number that ufw should listen on for incoming connections. This is typically used for SSH (port 22) or other services you want to allow access to. |
| `ufw_outgoing_traffic` | complex, see below | Allowed outgoing ports and protocols. |
| `ufw_rate_limit` | `false` | If True, rate limiting is enabled for incoming connections. |

`conntrack_sysctl_settings` default value:

```yaml
net.netfilter.nf_conntrack_max: 2000000
net.netfilter.nf_conntrack_tcp_loose: 0
```

`ufw_outgoing_traffic` default value:

```yaml
- port: 22
  proto: tcp
- 53
- port: 80
  proto: tcp
- port: 123
  proto: udp
- port: 443
  proto: tcp
- 853
- port: 4460
  proto: tcp
```

## Tasks

`tasks/main.yml` executes, in order:

1. Stat IPv6 status
2. Set IPv6 fact
3. Install epel-release on RedHat family
4. Set sysctl configuration directory as fact
5. Stat /usr/lib/sysctl.d/ exists
6. Set sysctl fact
7. Determine sysctl configuration directory
8. Install additional kernel modules
9. Add the nf_conntrack module
10. Stat nf_conntrack_tcp_be_liberal
11. Enable nf_conntrack_tcp_be_liberal to keep connections alive
12. Debian family UFW installation
13. RedHat family UFW installation
14. Get available physical interfaces
15. Set UFW IPT_SYSCTL
16. Get UFW status
17. Enable UFW and set default deny
18. Allow incoming from administrator networks
19. Set default deny
20. Enable and start the UFW service
21. Stat UFW rules
22. Create UFW rules
23. Set rate limit on physical interfaces
24. Allow outgoing specified ports
25. Deny IPv4 loopback network traffic
26. Deny IPv6 loopback network traffic
27. Allow loopback traffic in
28. Allow loopback traffic out
29. Delete unmanaged UFW rules
30. Configure conntrack sysctl

## Handlers

- Restart sysctl

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.ufw
```

## Tags

`cis`, `debian`, `disa`, `hardening`, `security`, `ubuntu`, `ufw`

## License

Apache-2.0
