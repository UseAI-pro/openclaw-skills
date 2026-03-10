# Contributing

This repo is a curated set of **OpenClaw skills** (Markdown-based), optimized for security-first workflows.

## Add a skill

1. Create a new folder: `skills/<slug>/`
2. Add `skills/<slug>/SKILL.md` with YAML frontmatter + Markdown body.

Frontmatter schema (example):

```yaml
---
name: permission-auditor
description: "Analyze OpenClaw skill permissions and explain security implications."
metadata:
  short-description: Explain requested skill permissions and flag over-privileged combinations.
  why: Keep skill permissions minimal and understandable before granting access.
  what: Provides a permission-analysis module for mapping declared access to actual task need.
  how: Uses permission-by-permission review plus dangerous-combination checks and least-privilege guidance.
  results: Produces a permission fit assessment with recommended minimal access scope.
  version: 1.0.0
  updated: "2026-03-10T00:00:00Z"
  jtbd-1: When I need to decide whether a skill is requesting more access than its job actually needs.
  audit:
    kind: module
    author: useclawpro
    category: Security
    trust-score: 96
    last-audited: "2026-02-05"
    permissions:
      file-read: true
      file-write: false
      network: false
      shell: false
---
```

Rules:
- Use **ASCII** for `name` and folder `slug`.
- Keep the description short (1–2 sentences).
- Do not include secrets, tokens, or private URLs in skill bodies.
- Treat any `network` or `shell` permission as high-risk; justify it in the skill text.

## Update catalog

From repo root:

```bash
node scripts/generate-catalog.mjs
```

This updates:
- `README.md` (skills table)
- `catalog/skills.md`
- `catalog/skills.json`
- `catalog/skills.csv`

Validate the normalized frontmatter contract:

```bash
python3 scripts/validate_skills.py
```

## Reporting malicious skills

If you find a suspicious skill in the OpenClaw ecosystem, open an issue using the **Report malicious skill** template.
