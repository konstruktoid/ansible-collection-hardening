# motd_news

Manage apt esm, motd-news and Ubuntu PRO.

## Requirements

- Ansible-core >= 2.18

## Supported platforms

| Platform | Versions |
| --- | --- |
| Debian | trixie |
| Ubuntu | resolute |

## Role variables

This role has no configurable variables.

## Tasks

`tasks/main.yml` executes, in order:

1. Manage apt esm, motd-news and Ubuntu PRO
2. Stat /etc/default/motd-news
3. Disable motd-news
4. Stat /etc/update-motd.d
5. Find update-motd.d files
6. Update motd permissions
7. Set /etc/update-motd.d permission
8. Stat /usr/bin/pro
9. Check apt_news status
10. Disable apt_news
11. Stat apt ESM hook
12. Remove apt ESM hook
13. Gather motd-news.service systemd unit status
14. Mask motd-news.service
15. Gather motd-news.timer systemd unit status
16. Mask motd-news.timer

## Example playbook

```yaml
- hosts: all
  become: true
  roles:
    - konstruktoid.hardening.motd_news
```

## Tags

`cis`, `disa`, `hardening`, `security`, `ubuntu`

## License

Apache-2.0
