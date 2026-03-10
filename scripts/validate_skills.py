#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / 'skills'
REQUIRED_TOP = ['name', 'description', 'metadata']
REQUIRED_METADATA = ['short-description', 'why', 'what', 'how', 'results', 'version', 'updated']
REQUIRED_AUDIT = ['kind', 'author', 'category', 'trust-score', 'last-audited', 'permissions']
REQUIRED_PERMISSIONS = ['file-read', 'file-write', 'network', 'shell']
SEMVER_RE = re.compile(r'^\d+\.\d+\.\d+$')
UPDATED_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')
DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')


def load_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n?', text)
    if not match:
        raise ValueError('missing frontmatter block')
    return yaml.safe_load(match.group(1)) or {}


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        frontmatter = load_frontmatter(path)
    except Exception as exc:
        return [f'{path}: {exc}']

    for key in REQUIRED_TOP:
        if key not in frontmatter:
            errors.append(f'{path}: missing top-level {key}')

    metadata = frontmatter.get('metadata') or {}
    for key in REQUIRED_METADATA:
        value = metadata.get(key)
        if value in (None, ''):
            errors.append(f'{path}: missing metadata.{key}')

    audit = metadata.get('audit') or {}
    for key in REQUIRED_AUDIT:
        value = audit.get(key)
        if value in (None, ''):
            errors.append(f'{path}: missing metadata.audit.{key}')

    perms = audit.get('permissions') or {}
    for key in REQUIRED_PERMISSIONS:
        if key not in perms:
            errors.append(f'{path}: missing metadata.audit.permissions.{key}')
        elif not isinstance(perms[key], bool):
            errors.append(f'{path}: metadata.audit.permissions.{key} must be boolean')

    version = metadata.get('version', '')
    if version and not SEMVER_RE.match(str(version)):
        errors.append(f'{path}: metadata.version must be semver')

    updated = metadata.get('updated', '')
    if updated and not UPDATED_RE.match(str(updated)):
        errors.append(f'{path}: metadata.updated must be UTC ISO8601 with Z suffix')

    last_audited = audit.get('last-audited', '')
    if last_audited and not DATE_RE.match(str(last_audited)):
        errors.append(f'{path}: metadata.audit.last-audited must be YYYY-MM-DD')

    trust_score = audit.get('trust-score')
    if trust_score is None:
        pass
    elif not isinstance(trust_score, int):
        errors.append(f'{path}: metadata.audit.trust-score must be integer')
    elif not 0 <= trust_score <= 100:
        errors.append(f'{path}: metadata.audit.trust-score must be between 0 and 100')

    for key in ['short-description', 'why', 'what', 'how', 'results', 'jtbd-1', 'jtbd-2', 'jtbd-3']:
        value = metadata.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(f'{path}: metadata.{key} must be string when present')

    for key in ['kind', 'author', 'category', 'last-audited']:
        value = audit.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(f'{path}: metadata.audit.{key} must be string')

    return errors


def main() -> int:
    errors: list[str] = []
    count = 0
    for skill_path in sorted(SKILLS_DIR.glob('*/SKILL.md')):
        count += 1
        errors.extend(validate_skill(skill_path))
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        print(f'Validation failed: {len(errors)} issue(s) across {count} skill(s)', file=sys.stderr)
        return 1
    print(f'Validated {count} skill(s)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
