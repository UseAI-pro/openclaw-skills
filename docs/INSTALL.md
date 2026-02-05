# Install (Codex CLI / Claude Code / OpenClaw)

This repo is a **skills pack**: each skill is a folder containing a `SKILL.md` file.

Important mental model:
- A skill is **instructions for an AI agent**.
- It doesn’t “run” by itself.
- You either **copy/paste** it into any LLM chat, or install it into a **skill-aware host**.

Two user-facing skills (start here):
- `skill-auditor` — Job 1: audit a skill before install
- `setup-auditor` — Job 2: audit your environment before running skills

Everything else in `skills/` is a **module** (a reusable checklist) used by the auditors and/or advanced users.

## Option 0 — No tooling (copy/paste)

If you just want the behavior *right now*:
1) open `skills/<skill>/SKILL.md`
2) copy/paste it into ChatGPT/Claude/etc
3) then paste the “target” you want it to work on (another `SKILL.md`, a config, a log, etc.)

This is the simplest way to use the “auditor” skills without installing anything.

## Option 1 — Codex CLI (global skills)

Typical location:
- `~/.codex/skills/<skill-name>/SKILL.md`

macOS/Linux (symlink):
```bash
git clone https://github.com/UseAI-pro/openclaw-skills-security.git
cd openclaw-skills-security

mkdir -p ~/.codex/skills
ln -s "$PWD/skills/skill-auditor" ~/.codex/skills/skill-auditor
ln -s "$PWD/skills/setup-auditor" ~/.codex/skills/setup-auditor
```

Expected result:
- after restarting Codex, the auditors appear in your available skills list (or become usable by name).

## Option 2 — Claude Code (project-local skills)

Typical location (inside your project):
- `.claude/skills/<skill-name>/SKILL.md`

macOS/Linux (symlink):
```bash
git clone https://github.com/UseAI-pro/openclaw-skills-security.git
cd openclaw-skills-security

mkdir -p .claude/skills
ln -s "$PWD/skills/skill-auditor" .claude/skills/skill-auditor
ln -s "$PWD/skills/setup-auditor" .claude/skills/setup-auditor
```

Expected result:
- after restarting Claude Code, the project skill is available and can be invoked by name.

## Option 3 — OpenClaw

OpenClaw hosts vary. The only invariant we rely on is:
- a skill is a folder containing `SKILL.md`

If your OpenClaw host supports loading local skills, point it at the `skills/` directory or copy individual skill folders into its configured “skills” path.

## Smoke test prompt

After installation, try:
- “Use `skill-auditor` to audit the SKILL.md below and return a SKILL AUDIT REPORT.”

Then paste any target `SKILL.md` (or a manifest JSON) to confirm the flow works end-to-end.
