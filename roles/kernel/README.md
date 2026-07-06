# kernel

Hardens kernel runtime behavior via sysctl and boot-time parameters: restricts virtual syscalls (vsyscall), enables page poisoning, kernel page-table isolation, SLUB debug poisoning, and kernel lockdown mode, using GRUB or grubby depending on the platform.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/kernel/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `allow_virtual_system_calls` | `true` | Allow virtual system calls (vsyscall). |
| `enable_page_poisoning` | `true` | Enable kernel page poisoning. |
| `kernel_lockdown` | `false` | Configures kernel_lockdown. |
| `page_table_isolation` | `true` | Enable page table isolation (PTI). |
| `slub_debugger_poisoning` | `false` | Enable SLUB debugger poisoning. |

## Tasks

`tasks/main.yml` executes, in order:

1. Configure Kernel parameters
2. Configure virtual system calls
3. Configure virtual system calls using grubby
4. Configure page poisoning
5. Configure page poisoning using grubby
6. Configure page table isolation
7. Configure page table isolation using grubby
8. Configure SLUB debugger poisoning
9. Configure SLUB debugger poisoning using grubby
10. Configure kernel lockdown
11. Set kernel lockdown mode as fact
12. Configure kernel lockdown mode
13. Configure kernel lockdown mode using grubby

## Handlers

- Update GRUB

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.kernel
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `kernel`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
