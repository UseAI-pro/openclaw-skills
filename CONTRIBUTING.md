# Contributing

This repo is a curated set of **OpenClaw skills** (Markdown-based), optimized for security-first workflows.

## Add a skill

1. Create a new folder: `skills/<slug>/`
2. Add `skills/<slug>/SKILL.md` with YAML frontmatter + Markdown body.

Frontmatter schema (example):

```yaml
---
name: permission-auditor
version: 1.0.0
description: "Analyze OpenClaw skill permissions and explain security implications."
author: useclawpro
category: Security
trustScore: 96
permissions:
  fileRead: true
  fileWrite: false
  network: false
  shell: false
lastAudited: "2026-02-05"
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

## Reporting malicious skills

If you find a suspicious skill in the OpenClaw ecosystem, open an issue using the **Report malicious skill** template.
