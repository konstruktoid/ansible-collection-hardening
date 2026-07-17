# firewalld

An Ansible role to manage firewalld default-deny zone rules.

## Requirements

- Ansible-core >= 2.18
- `ansible.posix` collection
- `community.general` collection

## Supported platforms

| Platform | Versions |
| --- | --- |
| AlmaLinux/EL | 10 |

## Role variables

Defined in `roles/firewalld/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `firewalld_zone` | `public` | The firewalld zone to set as default-deny and apply `firewalld_admin_net`/`firewalld_ports` to. |
| `firewalld_admin_net` | `["192.168.0.0/24", "192.168.1.0/24"]` | Only the network(s) defined in `firewalld_admin_net` are allowed to connect to `firewalld_ports`. |
| `firewalld_ports` | `[22]` | Specifies the port number(s) that firewalld should accept incoming connections on. This is typically used for SSH (port 22) or other services you want to allow access to. |
| `firewalld_log_denied` | `unicast` | `firewall-cmd --set-log-denied` value. One of `all`, `unicast`, `broadcast`, `multicast` or `off`. |
| `firewalld_rate_limit` | `false` | If True, rate limiting is enabled for incoming administrator connections. |
| `firewalld_rate_limit_value` | `6/m` | The firewalld rich rule `limit value` applied when `firewalld_rate_limit` is True. |
| `firewalld_conntrack_sysctl_settings` | mapping, see below | Netfilter connection tracking sysctl settings. |

`firewalld_conntrack_sysctl_settings` default value:

```yaml
net.netfilter.nf_conntrack_max: 2000000
net.netfilter.nf_conntrack_tcp_loose: 0
```

## Differences from the `ufw` role

This role is the AlmaLinux/EL counterpart to the `ufw` role, but firewalld's
zone model differs from ufw's in a way that changes what can be mirrored:

- firewalld zones (and thus the `DROP` zone target this role sets) only
  filter traffic **arriving on interfaces bound to the zone** (INPUT/FORWARD).
  Locally-originated (OUTPUT) traffic is not filtered by a zone target, so
  unlike `ufw`, this role does **not** implement default-deny egress
  filtering — there is no `firewalld_outgoing_traffic` equivalent.
  Egress control in firewalld requires policy objects (`firewall-cmd
  --new-policy`), which `ansible.posix.firewalld` does not currently expose;
  adding that would mean managing state by hand with raw `firewall-cmd`
  calls, which was judged too fragile to take on here.
- Loopback traffic is never bound to a zone, so there is no equivalent of
  ufw's explicit "allow loopback in/out" rules.
- The administrator-network rich rule is always applied before the zone
  target is set to `DROP`, so a playbook run connecting over one of
  `firewalld_ports` cannot lock itself out mid-run.
- The zone's default services (e.g. `ssh`, `dhcpv6-client` in `public`) are
  always accepted regardless of the zone target, so this role removes
  whatever services are enabled on `firewalld_zone` by default. Otherwise
  they would bypass the administrator-network rich rule and allow SSH from
  anywhere, the same class of mistake `ufw`'s explicit allow-list avoids.

## Tasks

`tasks/main.yml` executes, in order:

1. Determine sysctl configuration directory
2. Install firewalld packages
3. Add the nf_conntrack module
4. Enable nf_conntrack_tcp_be_liberal to keep connections alive
5. Enable and start the firewalld service
6. Remove default zone services
7. Set log-denied packets
8. Allow incoming from administrator networks
9. Set default zone target to DROP
10. Configure conntrack sysctl

## Handlers

- Restart sysctl

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.firewalld
```

## Tags

`almalinux`, `centos`, `cis`, `disa`, `firewalld`, `hardening`, `security`, `system`, `systemd`

## License

Apache-2.0
