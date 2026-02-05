# Threat Coverage Matrix

> Evidence: which checks catch which real-world attacks.

## Source Data

- **22 curated threats** from UseClaw malicious skills database
- **341 malicious skills** from ClawHavoc campaign (Jan-Feb 2026)

## Real Attack Types

| # | Attack Type | Real Examples | Frequency |
|---|---|---|---|
| T1 | Typosquatting | gihub-push, github-pusher, code-reveiw, docs-writer | 36% of curated |
| T2 | Credential theft | env-backup, cloud-sync-pro, project-stats | 14% |
| T3 | Crypto miners | build-optimizer-turbo, perf-boost | 9% |
| T4 | Reverse shells | remote-debug-helper, ssh-manager | 9% |
| T5 | Prompt injection | prompt-enhance, context-boost | 9% |
| T6 | Skill loader exploits | skill-loader-patch, auto-update-fix | 9% |
| T7 | Obfuscated commands | (ClawHavoc campaign) | common |
| T8 | Supply chain attack | (ClawHub ecosystem) | common |
| T9 | Social engineering | (trust exploitation) | common |
| T10 | Persistence | .bashrc modification, authorized_keys injection | 9% |
| T11 | Over-privilege | full system access without justification | 5% |
| T12 | Data exfiltration | network POST with file/env content | 14% |

## Coverage by Auditor

### skill-auditor catches:

| Step | Threats Covered | Primary For |
|---|---|---|
| Step 1: Metadata & Typosquat | T1 | T1 Typosquatting |
| Step 2: Permission Analysis | T4, T11, T12 | T11 Over-privilege |
| Step 3: Dependency Audit | T1, T6, T7, T8 | T6 Loader exploits, T8 Supply chain |
| Step 4: Prompt Injection | T5, T7, T9 | T5 Prompt injection, T9 Social eng |
| Step 5: Network Analysis | T4, T7, T12 | T4 Reverse shells, T12 Exfil |
| Step 6: Content Red Flags | T1, T2, T4, T5, T7 | General |

**Total: 10/12 threat types covered**

### setup-auditor catches:

| Step | Threats Covered | Primary For |
|---|---|---|
| Step 1: Credential Scan | T2, T12 | T2 Credential theft |
| Step 2: Config Audit | T10, T11 | T10 Persistence |
| Step 3: Sandbox Readiness | T3, T4, T6 | T3 Crypto miners |
| Step 4: Persistence Check | T10 | T10 Persistence |

**Total: 7/12 threat types covered**

### Combined coverage: 12/12 threat types
