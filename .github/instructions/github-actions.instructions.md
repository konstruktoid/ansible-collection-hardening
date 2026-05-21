---
applyTo: ".github/workflows/**/*.yml,.github/workflows/**/*.yaml,**/action.yml,.github/actions/**/*.yml,.github/actions/**/*.yaml"
---

# Enterprise GitHub Actions Security Instructions

Apply these rules to workflow and action definitions.

## Security-first workflow design
- Use least-privilege `permissions` at workflow/job scope; avoid implicit broad defaults.
- Keep triggers narrow (`branches`, `paths`, event types) and avoid unnecessary execution scope.
- Pin third-party actions to commit SHA where possible.
- Treat all PR metadata, artifact contents, and external inputs as untrusted.

## Secrets and token handling
- Never hardcode secrets or tokens.
- Use GitHub secrets/variables and mask sensitive output.
- Avoid printing env/context objects that may contain credentials.
- Minimize `GITHUB_TOKEN` privileges and step exposure.

## High-risk event and runner handling
- Use extreme caution with `pull_request_target` and `workflow_run`; never execute untrusted code with elevated context.
- For self-hosted runners, enforce strict trust boundaries, labeling, and job scoping.
- Validate artifact provenance before reuse; avoid cross-trust artifact promotion.
- Treat caches as potentially attacker-influenced; scope keys defensively.

## Reliability and safety defaults
- Set explicit `timeout-minutes`.
- Use `concurrency` to prevent unsafe overlap when deployments/stateful steps exist.
- Keep scripts short, fail-fast, and explicit (`set -euo pipefail` for bash steps where appropriate).
- Avoid curl-pipe-to-shell patterns; download, verify, then execute.

## Review priorities
1. Privilege model (`permissions`, token use, OIDC scope)
2. Trigger safety and untrusted input handling
3. Third-party dependency trust (pinning, provenance)
4. Secret exposure risks in logs, outputs, artifacts, and caches
5. Runner isolation and escalation paths

## Risk levels
- Critical: direct secret exfiltration path or untrusted-code execution in privileged context
- High: broad token permissions, unsafe event usage, or unpinned high-trust action usage
- Medium: missing safety controls (`timeout-minutes`, `concurrency`, validation gaps)
- Low: style/maintainability issues with limited security impact
