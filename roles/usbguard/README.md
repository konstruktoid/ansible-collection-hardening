# usbguard

Ansible role to manage USBGuard, a software for implementing USB device authorization policies.

## Requirements

- Ansible-core >= 2.18
- `community.general` collection

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| EL | 10 |
| Ubuntu | noble, resolute |

## Role variables

Defined in `roles/usbguard/defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `usbguard_auditbackend` | `"LinuxAudit"` | USBGuard audit events log backend. |
| `usbguard_auditfilepath` | `"/var/log/usbguard/usbguard-audit.log"` | USBGuard audit events log file path. |
| `usbguard_authorizeddefault` | `"none"` | Default authorized controller devices. |
| `usbguard_configuration_file` | `"/etc/usbguard/usbguard-daemon.conf"` | USBGuard configuration file path. |
| `usbguard_devicemanagerbackend` | `"uevent"` | Which device manager backend implementation to use. |
| `usbguard_deviceruleswithport` | `false` | Generate device specific rules including the 'via-port' attribute. |
| `usbguard_hidepii` | `false` | Hide personally identifiable information such as device serial numbers and hashes of descriptors from audit entries. |
| `usbguard_implicitpolicytarget` | `"block"` | How to treat USB devices that don’t match any rule in the policy. |
| `usbguard_inserteddevicepolicy` | `"apply-policy"` | How to treat USB devices that are already connected after the daemon starts. |
| `usbguard_ipcaccesscontrolfiles` | `"/etc/usbguard/IPCAccessControl.d/"` | The files at this location will be interpreted by the daemon as IPC access control definition files. |
| `usbguard_ipcallowedgroups` | `["plugdev", "root", "wheel"]` | A list of groupnames that the daemon will accept IPC connections from. |
| `usbguard_ipcallowedusers` | `["root"]` | A list of usernames that the daemon will accept IPC connections from. |
| `usbguard_presentcontrollerpolicy` | `"keep"` | How to treat USB controller devices that are already connected when the daemon starts. |
| `usbguard_presentdevicepolicy` | `"apply-policy"` | How to treat USB devices that are already connected when the daemon starts. |
| `usbguard_restorecontrollerdevicestate` | `false` | Control whether the daemon will try to restore the attribute values to the state before modification on shutdown. |
| `usbguard_rulefile` | `"/etc/usbguard/rules.conf"` | USBGuard rule file path. |

## Tasks

`tasks/main.yml` executes, in order:

1. Stat USB device directory
2. Install and configure USBGuard
3. Debian family USBGuard installation
4. RedHat family USBGuard package installation
5. Suse family USBGuard package installation
6. Configure RuleFile
7. Configure ImplicitPolicyTarget
8. Configure PresentDevicePolicy
9. Configure PresentControllerPolicy
10. Configure InsertedDevicePolicy
11. Configure AuthorizedDefault
12. Configure RestoreControllerDeviceState
13. Configure DeviceManagerBackend
14. Configure IPCAllowedUsers
15. Configure IPCAllowedGroups
16. Configure IPCAccessControlFiles
17. Configure DeviceRulesWithPort
18. Configure AuditBackend
19. Configure AuditFilePath
20. Configure HidePII
21. Manage USBGuard service
22. Start and enable USBGuard
23. List all USBGuard rules
24. Generate USBGuard policy
25. Write policy and restart USBGuard
26. Write policy
27. Restart USBGuard

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.usbguard
```

## Tags

`almalinux`, `centos`, `cis`, `debian`, `disa`, `hardening`, `security`, `system`, `systemd`, `ubuntu`

## License

Apache-2.0
