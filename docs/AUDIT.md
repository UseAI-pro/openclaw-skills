# Audit workflow (fast → deep)

Goal: **decide if a skill is safe to install** (or if it should be blocked / sandboxed / reported).

Mental model:
- Installing a skill is **equivalent to running untrusted code** under your user account.
- This repo provides **auditor skills** you can use in a host agent or via copy/paste.

Start with the auditors:
- `skills/skill-auditor/SKILL.md` — Job 1: audit a skill before install
- `skills/setup-auditor/SKILL.md` — Job 2: audit your environment before running skills

The other folders under `skills/` are **modules** (reusable checklists) that auditors reference and advanced users can run directly.

## Inputs you can audit

You may have one of:
- **Skill name** (e.g., `git-commit-helper`)
- **Skill URL** (ClawHub / GitHub)
- **Manifest JSON**
- A local folder containing `SKILL.md` (+ optional code files)

## Fast check (2 minutes)

**Action:** paste the input into the browser verifier:
- https://useclaw.pro/verifier/

**Result:** you get:
- a verdict (SAFE / WARNING / DANGER / MALICIOUS)
- a trust score (heuristic)
- a permissions summary (file/network/shell)
- red flags (rules matched)

If verdict is **DANGER/MALICIOUS** → stop and report (see bottom).

## Deep check (10–20 minutes)

Use the “main auditor” skill (Job 1):
- `skills/skill-auditor/SKILL.md`

### Step 1 — Manifest sanity (Result A)

Open the target `SKILL.md` and check:
- name (typosquatting risk)
- author identity (is there a real repo/profile?)
- version history (does it look maintained?)
- description matches what it claims to do

**Result A:** you have a short list of “this is plausible” vs “this is suspicious”.

### Step 2 — Permissions fit (Result B)

Ask: “does this skill *need* these permissions?”

High‑risk combinations:
- `network` + `shell` (exfiltration is easy)
- broad file reads (home folders, dotfiles)
- install hooks / auto‑run behavior

**Result B:** you have “permissions justified?” yes/no, plus what to deny.

### Step 3 — Red flags in content (Result C)

Look for:
- credential paths (`~/.ssh`, `~/.aws`, `.env`)
- “curl | bash”, `wget`, reverse shell patterns
- obfuscated or base64 payloads
- instructions to disable sandbox/safety
- unknown URLs / IPs

**Result C:** you have a list of red flags by severity.

### Step 4 — Verdict & next step (Result D)

Produce a report (recommended format):

```
SKILL AUDIT REPORT
==================
Skill: <name>
Source: <url/path>

VERDICT: SAFE / WARNING / DANGER / BLOCK

WHY:
- ...

PERMISSIONS:
- fileRead:  needed/not needed — why
- fileWrite: needed/not needed — why
- network:   needed/not needed — endpoints?
- shell:     needed/not needed — commands?

RED FLAGS:
- [critical] ...
- [high] ...
- [medium] ...

NEXT:
- install in sandbox / do not install / report suspicious
```

## Optional: run a single module (advanced)

If you want a focused check (instead of the full auditor protocol), run a module directly:
- Permissions fit → `skills/permission-auditor/SKILL.md`
- Prompt injection → `skills/prompt-guard/SKILL.md`
- Supply chain → `skills/dependency-auditor/SKILL.md`
- Network/exfil → `skills/network-watcher/SKILL.md`

## “Audit without installing” (copy/paste prompt)

If you don’t have a host tool installed yet, you can still do a full audit:
1) paste `skills/skill-auditor/SKILL.md` into any LLM
2) paste the target `SKILL.md`
3) ask for the report format above

This keeps you in a safe “review” mode before you install anything.

## Report suspicious / malicious skills

Open an issue with sanitized evidence (no secrets):
- https://github.com/UseAI-pro/openclaw-skills-security/issues/new?template=report-malicious-skill.md
