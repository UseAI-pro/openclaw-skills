---
name: "Report malicious skill"
about: "Report a suspicious/malicious OpenClaw skill (research only)."
title: "[malicious-skill] <skill-name-or-url>"
labels: ["security", "malicious-skill"]
---

## Skill

- Name / slug:
- URL(s):
- Where discovered:
- Date (UTC):

## Why suspicious

- [ ] Typosquatting / impersonation
- [ ] Exfiltration behavior (network)
- [ ] Install hooks / persistence
- [ ] Shell execution
- [ ] Reads secrets (`.env`, `~/.ssh`, `~/.aws`, etc.)
- [ ] Obfuscation
- [ ] Other:

## Evidence (sanitized)

Paste **sanitized** evidence (no secrets):
- excerpts of manifest / permissions requested
- suspicious domains / IPs
- suspicious commands

## Suggested mitigation

- [ ] Blocklist candidate
- [ ] Needs review / reproduce safely
- [ ] Add heuristic rule

