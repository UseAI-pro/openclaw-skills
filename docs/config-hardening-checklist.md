# Config Hardening Checklist

> Minimum security baseline for running OpenClaw skills safely.

## P0 (do today)

- [ ] **Create AGENTS.md** with explicit allowed/forbidden actions
- [ ] **Set `network: none`** as default for all skills
- [ ] **Set `shell: prompt`** (require confirmation for every command)
- [ ] **Add to .gitignore**: `.env`, `*.pem`, `*.key`, `.ssh/`, `.aws/`
- [ ] **Enable sandbox mode** for untrusted skills

## P1 (this week)

- [ ] Audit all installed skills with `skill-auditor`
- [ ] Set up Docker sandbox profile (see `setup-auditor`)
- [ ] Configure file access allowlists (project dirs only)
- [ ] Disable mDNS broadcasting (gateway config)
- [ ] Enable HTTPS for remote access
- [ ] Configure rate limiting

## AGENTS.md Template

```markdown
# Security Policy

## Allowed (no confirmation)
- Read files in current project directory
- Write files in src/, tests/, docs/
- Read-only git commands (status, log, diff)

## Requires Confirmation
- Any shell command that modifies files
- Git commits and pushes
- Installing dependencies
- File operations outside project directory

## Forbidden (never)
- Read ~/.ssh, ~/.aws, ~/.gnupg, ~/.config/gh
- Read .env files outside current project
- Network requests to undeclared domains
- Execute downloaded scripts
- Modify system config files
- Disable sandbox or security settings
- Run as root/sudo
```

## Dangerous Permission Combinations

| Combination | Risk | Action |
|---|---|---|
| `network` + `fileRead` | CRITICAL | Exfiltration — deny unless justified |
| `network` + `shell` | CRITICAL | Full remote access — deny |
| `shell` + `fileWrite` | HIGH | Persistence — require sandbox |
| All four permissions | CRITICAL | Full system access — deny |
