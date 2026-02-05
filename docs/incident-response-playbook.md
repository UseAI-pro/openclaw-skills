# Incident Response Playbook

> What to do if you suspect a malicious skill was installed or your OpenClaw setup was compromised.

## Severity Levels

| Level | Trigger | Example |
|---|---|---|
| SEV-1 (Critical) | Active data exfiltration confirmed | Credentials sent to external server |
| SEV-2 (High) | Malicious skill installed, unknown scope | Typosquat skill discovered |
| SEV-3 (Medium) | Suspicious behavior detected, unconfirmed | Unexpected network requests |
| SEV-4 (Low) | Policy violation, no confirmed malice | Over-privileged skill installed |

## Phase 1: Containment (do first)

1. **Stop the skill** — remove from config, kill background processes
2. **Disconnect network** if exfiltration suspected
3. **Preserve evidence** — save the malicious SKILL.md, logs, timestamps
4. **Revoke API tokens** the skill had access to

## Phase 2: Investigation

**What did the skill access?**
- Which files? (especially `.env`, `.ssh`, `.aws`)
- Network requests? To which endpoints?
- Shell commands? Which ones?
- File modifications?

**Was persistence established?**
- `~/.bashrc`, `~/.zshrc`, `~/.profile`
- `~/.ssh/authorized_keys`
- `crontab -l`
- `.git/hooks/`
- Node.js `postinstall` scripts

## Phase 3: Credential Rotation

**Rotate immediately (SEV-1/2):**
- [ ] API keys in `.env`
- [ ] Cloud provider keys (AWS, GCP, Azure)
- [ ] GitHub/GitLab tokens
- [ ] Database passwords
- [ ] SSH keys

**Rotate within 24h:**
- [ ] Service account credentials
- [ ] CI/CD pipeline secrets
- [ ] Third-party API keys

## Phase 4: Recovery

1. Remove malicious skill and all traces
2. Restore modified files from git
3. Run `setup-auditor` to verify clean state
4. Enable sandbox mode for all future skills

## Phase 5: Report

Document: date, severity, skill name, exposure duration, compromised data, actions taken, lessons learned.

Report the skill:
- ClawHub (for removal)
- UseClawPro (for database update)
- OpenClaw security team (if CVE applies)
