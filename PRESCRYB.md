# Using prescryb with this collection

[`prescryb`](https://github.com/konstruktoid/prescryb) is a companion MCP
server: a remediation orchestrator that connects to a host over SSH,
inventories its packages, matches them against known CVEs, maps
insecure-configuration areas to CIS/DISA STIG topics and
`konstruktoid.hardening` roles, and can render a suggest-only Ansible
playbook from the findings. It never applies changes to the target host;
every tool is read-only or produces text or data only.

It pairs naturally with this collection. Harden a host with
`konstruktoid.hardening` roles, then use `prescryb` to check what remains
outstanding (unpatched packages, missing controls) and get remediation
suggestions that reference the roles already in this repository.

## Install

```console
git clone https://github.com/konstruktoid/prescryb
cd prescryb
uv sync
```

Register it with an MCP client:

```console
claude mcp add prescryb -- uv --directory /path/to/prescryb run prescryb
```

Or, for Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "prescryb": {
      "command": "uv",
      "args": ["--directory", "/path/to/prescryb", "run", "prescryb"]
    }
  }
}
```

## Tools

| Tool | What it does |
| --- | --- |
| `inventory_host` | Connects over SSH, detects the distribution, and lists installed packages with versions. |
| `check_cves` | Batch-matches package versions against [OSV.dev](https://osv.dev), with ecosystem-aware matching rather than name-only matching. |
| `fetch_advisory` | Fetches the current NVD record for one CVE. |
| `map_compliance` | Maps a free-text topic (for example, `"ssh"`, `"sudo"`, `"kernel modules"`) to CIS/DISA STIG topic areas, the matching `konstruktoid.hardening` role if one exists, and the MITRE ATT&CK techniques and mitigations it addresses. |
| `lookup_cce` / `list_cce_targets` | Returns NIST Common Configuration Enumeration entries for a platform. Coverage is limited to RHEL-family and SUSE; Debian, Ubuntu, Alpine, and Arch have no upstream CCE data. |
| `generate_playbook` | Renders a suggest-only Ansible playbook: CVE fixes become package-upgrade tasks, and compliance areas become `roles:` references into this collection where a match exists. |

Typical workflow: `inventory_host`, then `check_cves`, then optionally
`fetch_advisory` on relevant CVEs, then `map_compliance` (and `lookup_cce`)
for insecure-configuration areas, then `generate_playbook`.

## Pointing it at a molecule instance

This collection's `default` molecule scenario boots real VMs using
`qemu-system-x86_64` rather than containers, making them reachable over
plain SSH. This makes it a suitable target for exercising `prescryb` after a
converge:

```console
molecule converge -s default
```

Each platform in `extensions/molecule/default/molecule.yml` forwards its own
local SSH port (`ssh_port: 22201` for `almalinux10`, `22202` for `resolute`,
`22203` for `trixie`) to the guest's `sshd`, with a per-run ephemeral key
under `~/.ansible/tmp/molecule.<hash>.default/ssh_key`. An MCP client can
inventory a host directly, with no `~/.ssh/config` entry required:

> Inventory 127.0.0.1, port 22201, user almalinux, identity_file
> `~/.ansible/tmp/molecule.<hash>.default/ssh_key`. Check installed
> packages, find CVEs, suggest a fix in Ansible if possible, and identify
> the compliance controls it maps to.

`inventory_host` rejects unknown host keys unless `trust_unknown_host=True`
is passed. For a local, ephemeral, newly created VM, this is normally safe
to set. Alternatively, pin the key once with a plain `ssh -p <port>
<user>@localhost`.

Run `molecule destroy -s default` when finished; `prescryb` does not
perform this step.

## Caveats observed in practice

- **CVE-matching coverage is uneven.** OSV.dev's coverage is mature for
  Debian, Ubuntu, and Alpine, but thinner for RHEL-family distributions
  (AlmaLinux, Rocky). `check_cves` returns a `warning` field on thinner
  ecosystems, and an empty result there should be treated as "not
  checked," not "clean."
- **Debian and Ubuntu results include many severity-`UNKNOWN`,
  low-relevance entries**, for example decade-old CVEs that the Debian
  security tracker still lists as present but unfixed against a source
  package, even when there is no practical exploitability. Review the
  packages that matter most (`curl`, `openssh`, `sudo`, `xz-utils`,
  kernel) rather than treating the raw match count as a severity signal.
- **Review generated playbooks before applying them.** The `roles:` list
  produced by `generate_playbook` can reference a role name that does not
  exist in this collection, for example `konstruktoid.hardening.pam`;
  there is no `pam` role here, since PAM hardening lives in
  `password_management` and `login_defs`. The tool's own header states
  "suggest-only, review with `ansible-playbook --check --diff`"; treat
  that instruction literally.

## Example result

Run against a fresh `molecule converge -s default` (AlmaLinux 10.2, Ubuntu
26.04 "resolute", Debian 13 "trixie"), 2026-07-09.

### almalinux10

`inventory_host` found 414 installed packages. `check_cves` against the
security-relevant subset (openssh, openssl, sudo, kernel, glibc, systemd,
curl, postfix, grub2, NetworkManager, vim, and others) returned 22
matches. OSV flagged AlmaLinux's ecosystem coverage as thinner than
Debian's or Ubuntu's, so the absence of a finding elsewhere is not proof
of a clean result. Notable findings:

| Package | Installed | Fixed | Advisory | Severity |
| --- | --- | --- | --- | --- |
| `openssl` / `openssl-libs` | 3.5.5-4.el10_2.alma.1 | 3.5.5-4.el10_2.alma.1 | ALSA-2026:25237 (CVE-2026-34180/1/2/3) | Important |
| `postfix` | 3.8.5-10.el10_2 | 2:3.8.5-10.el10_2 | ALSA-2026:25930 (CVE-2026-43964) | Important |
| `xz` / `xz-libs` | 5.6.2-4.el10_0 | 1:5.6.2-4.el10_0 | ALSA-2025:7524 (CVE-2025-31115) | Important |
| `tar` | 1.35-11.el10 | 2:1.35-9.el10_1 | ALSA-2026:0002 (CVE-2025-45582) | Moderate |
| `vim-minimal` | 9.1.083-9.el10_2.4 | 2:9.1.083-9.el10_2.2 | ALSA-2026:19073 (CVE-2026-34982) | Important |
| `grub2-common` | 2.12-46.el10_2.alma.1 | 1:2.12-29.el10_1.2.alma.1 | ALSA-2026:4649 (CVE-2025-61662) | Moderate |
| `shadow-utils` | 4.15.0-11.el10 | 2:4.15.0-8.el10 | ALSA-2025:20145 (CVE-2024-56433) | Low |

`map_compliance("ssh")` and `map_compliance("sudo")` both resolved to their
matching roles in this repository (`roles/ssh`, `roles/sudo`), plus MITRE
ATT&CK `T1021.004` (Remote Services: SSH, mitigation M1042), `T1110`
(Brute Force, mitigation M1032), and `T1548.003` (Sudo and Sudo Caching,
mitigation M1026).

`generate_playbook` for the five findings above, plus `compliance_areas:
["ssh", "sudo", "kernel modules", "password policy"]`, produced:

```yaml
# Generated by prescryb - SUGGESTION ONLY. Review with `ansible-playbook --check --diff`
# before applying; prescryb does not execute playbooks itself.
# Target: localhost  (almalinux 10.2, family=redhat)
#
# ALSA-2026:25237 (Important) on openssl: openssl security update
# ALSA-2026:25930 (Important) on postfix: postfix security update
# ALSA-2025:7524 (Important) on xz: xz security update
# ALSA-2026:0002 (Moderate) on tar: tar security update
# ALSA-2026:19073 (Important) on vim-minimal: vim security update
#
# Compliance mapping (CIS / DISA STIG topic areas - see role docs for specifics):
#   ssh: konstruktoid.hardening role 'ssh' found at .../roles/ssh
#   sudo: konstruktoid.hardening role 'sudo' found at .../roles/sudo
#   sysctl / kernel / kernel_modules / password_management / login_defs: found
#   pam: not found in konstruktoid/ansible-collection-hardening
#
# MITRE ATT&CK mapping (techniques mitigated by this change):
#   T1021.004 Remote Services: SSH | mitigation M1042
#   T1110 Brute Force | mitigation M1032
#   T1548.003 Sudo and Sudo Caching | mitigation M1026
#   T1068 Exploitation for Privilege Escalation | mitigation M1050
#   T1547.006 Kernel Modules and Extensions | mitigation M1047
#   T1078 Valid Accounts | mitigation M1032
---
- name: prescryb remediation for almalinux10
  hosts: almalinux10
  become: true
  tasks:
    - name: Upgrade openssl -> 1:3.5.5-4.el10_2.alma.1 (ALSA-2026:25237)
      ansible.builtin.dnf:
        name: openssl-1:3.5.5-4.el10_2.alma.1
        state: present
      tags: [prescryb, cve, alsa-2026:25237]
    - name: Upgrade postfix -> 2:3.8.5-10.el10_2 (ALSA-2026:25930)
      ansible.builtin.dnf:
        name: postfix-2:3.8.5-10.el10_2
        state: present
      tags: [prescryb, cve, alsa-2026:25930]
    - name: Upgrade xz -> 1:5.6.2-4.el10_0 (ALSA-2025:7524)
      ansible.builtin.dnf:
        name: xz-1:5.6.2-4.el10_0
        state: present
      tags: [prescryb, cve, alsa-2025:7524]
    - name: Upgrade tar -> 2:1.35-9.el10_1 (ALSA-2026:0002)
      ansible.builtin.dnf:
        name: tar-2:1.35-9.el10_1
        state: present
      tags: [prescryb, cve, alsa-2026:0002]
    - name: Upgrade vim-minimal -> 2:9.1.083-9.el10_2.2 (ALSA-2026:19073)
      ansible.builtin.dnf:
        name: vim-minimal-2:9.1.083-9.el10_2.2
        state: present
      tags: [prescryb, cve, alsa-2026:19073]
  roles:
    - konstruktoid.hardening.kernel
    - konstruktoid.hardening.kernel_modules
    - konstruktoid.hardening.login_defs
    - konstruktoid.hardening.password_management
    - konstruktoid.hardening.ssh
    - konstruktoid.hardening.sudo
    - konstruktoid.hardening.sysctl
```

### resolute (Ubuntu 26.04)

Filtered `check_cves` (163 security-relevant packages out of 650 installed)
returned 8 matches, all against `curl` 8.18.0-1ubuntu2.2 and `gnupg2`
2.4.8-4ubuntu3, with real CVSS vectors in this case, since OSV's Ubuntu
coverage is better than AlmaLinux's:

| CVE | Package | CVSS vector | Summary |
| --- | --- | --- | --- |
| CVE-2026-10536 | curl | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | Use-after-free in HTTP/2 stream-dependency handling after `curl_easy_reset()`. |
| CVE-2026-11352 | curl | `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H` | QUIC UDP zero-length-datagram flood causing client denial of service. |
| CVE-2026-11856 | curl | `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` | Digest `Authorization:` header leaked across origin change on handle reuse. |
| CVE-2026-8932 | curl | `AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N` | Connection reuse ignores changed mTLS or client-certificate options. |
| CVE-2026-57062 | gnupg2 | `AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N` | CMS/AES-GCM ICV length mishandled in `gpgsm`. |

### trixie (Debian 13)

Filtered `check_cves` (85 security-relevant packages out of 392 installed)
returned 128 matches, all severity `UNKNOWN`, which is typical for
Debian's OSV export, since CVSS is not attached to most Debian
security-tracker entries. Match volume by package:

| Package | Matches |
| --- | --- |
| `vim` | 36 |
| `curl` | 30 |
| `python3.13` | 15 |
| `perl` | 12 |
| `libxml2` | 7 |
| `systemd` | 5 |
| `wget` | 5 |
| `gnupg2` | 4 |
| others (`coreutils`, `libgcrypt20`, `rsyslog`, `tar`, `tcpdump`, `iptables`, `socat`, `sudo`, `xz-utils`) | 1-2 each |

Most of these entries are the low-relevance, tracker-listed-but-not-
necessarily-exploitable noise described in Caveats above, for example
`CVE-2005-1119` against `sudo` and `CVE-2013-4392` against `systemd`. The
one worth tracking: `xz-utils` 5.8.1-1 is affected by **CVE-2026-34743**, a
buffer overflow in `lzma_index_decoder()` for a crafted zero-record Index,
fixed upstream in 5.8.3 but not yet present in this `trixie` snapshot's
package version at scan time.

### NIST CCE lookup (AlmaLinux: `rhel8`)

AlmaLinux 10 has no dedicated CCE export; the closest usable target is
`rhel8`. `lookup_cce(target="rhel8", keyword="ssh")` returned 58 matches
(29 shown, truncated), including concrete, actionable checks beyond what
`map_compliance`'s topic-level mapping provides, for example:

- `CCE-82901-0` / `CCE-82898-8` / `CCE-82894-7`: `/etc/ssh/sshd_config`
  should be owned by `root:root`, mode `0600`.
- `CCE-82424-3`: SSH host private keys should be mode `0640`.
- `CCE-82176-9` / `CCE-82225-4`: SSHD and SSH-client crypto policy should
  not be overridden away from the system-wide crypto-policies setting.
- `CCE-80953-3`: `kernel.yama.ptrace_scope = 1` to prevent compromised
  binaries from tracing other processes' SSH sessions.

Compare these against what `roles/ssh` and `roles/sysctl` in this
collection already enforce before treating any of these as a gap.
