# Security

If you believe you have found a security issue related to this repository:

- Do **not** post secrets in public issues.
- Prefer reporting via a GitHub issue with sanitized details, or contact the maintainers privately if credentials may be involved.

## Scope

This repository contains **Markdown skill definitions**. Treat every third-party skill as **untrusted code** until reviewed, even if it looks harmless.

Recommended baseline:
- Run OpenClaw in a sandbox (container/VM)
- Default `network: none`
- Keep `shell: prompt`
- Keep secrets isolated (`.env`, `~/.ssh`, cloud creds)

