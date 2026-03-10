#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / 'skills'
CATALOG_DIR = ROOT / 'catalog'
README_PATH = ROOT / 'README.md'


def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n?', text)
    if not match:
        raise ValueError(f'Missing frontmatter in {path}')
    frontmatter = yaml.safe_load(match.group(1)) or {}
    body = text[match.end():]
    return frontmatter, body


def perms_to_short(perms: dict) -> str:
    parts = []
    if perms.get('file-read') is True:
        parts.append('R')
    if perms.get('file-write') is True:
        parts.append('W')
    if perms.get('network') is True:
        parts.append('Net')
    if perms.get('shell') is True:
        parts.append('Sh')
    return ','.join(parts) if parts else '-'


def kind_rank(kind: str) -> int:
    if kind == 'auditor':
        return 0
    if kind == 'module':
        return 1
    return 2


def flatten_skill(slug: str, path: Path, frontmatter: dict) -> dict:
    metadata = frontmatter.get('metadata') or {}
    audit = metadata.get('audit') or {}
    permissions = audit.get('permissions') or {}
    return {
        'name': frontmatter.get('name', ''),
        'slug': slug,
        'description': frontmatter.get('description', ''),
        'short_description': metadata.get('short-description', ''),
        'why': metadata.get('why', ''),
        'what': metadata.get('what', ''),
        'how': metadata.get('how', ''),
        'results': metadata.get('results', ''),
        'version': metadata.get('version', ''),
        'updated': metadata.get('updated', ''),
        'jtbd_1': metadata.get('jtbd-1', ''),
        'jtbd_2': metadata.get('jtbd-2', ''),
        'jtbd_3': metadata.get('jtbd-3', ''),
        'audit_kind': audit.get('kind', ''),
        'audit_author': audit.get('author', ''),
        'audit_category': audit.get('category', ''),
        'audit_trust_score': audit.get('trust-score', ''),
        'audit_last_audited': audit.get('last-audited', ''),
        'audit_permission_file_read': permissions.get('file-read', False),
        'audit_permission_file_write': permissions.get('file-write', False),
        'audit_permission_network': permissions.get('network', False),
        'audit_permission_shell': permissions.get('shell', False),
        'path': str(path.relative_to(ROOT)),
    }


def load_skills() -> list[dict]:
    skills = []
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        skill_path = skill_dir / 'SKILL.md'
        frontmatter, _ = load_frontmatter(skill_path)
        if not frontmatter.get('name'):
            continue
        skills.append(flatten_skill(skill_dir.name, skill_path, frontmatter))

    skills.sort(
        key=lambda item: (
            kind_rank(str(item['audit_kind'])),
            -(int(item['audit_trust_score']) if str(item['audit_trust_score']).isdigit() else -1),
            item['slug'],
        )
    )
    return skills


def markdown_table(skills: list[dict]) -> str:
    header = [
        '| Skill | Type | Category | Trust | Perms | Last audited | Version |',
        '| --- | --- | --- | ---: | --- | --- | --- |',
    ]
    rows = []
    for item in skills:
        rows.append(
            f"| [{item['slug']}]({item['path']}) | {item['audit_kind']} | {item['audit_category']} | {item['audit_trust_score']} | {perms_to_short({'file-read': item['audit_permission_file_read'], 'file-write': item['audit_permission_file_write'], 'network': item['audit_permission_network'], 'shell': item['audit_permission_shell']})} | {item['audit_last_audited']} | {item['version']} |"
        )
    return '\n'.join(header + rows) + '\n'


def update_readme(table_md: str) -> None:
    readme = README_PATH.read_text(encoding='utf-8')
    start = '<!-- catalog:start -->'
    end = '<!-- catalog:end -->'
    start_idx = readme.find(start)
    end_idx = readme.find(end)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise RuntimeError('README.md is missing catalog markers')
    before = readme[: start_idx + len(start)]
    after = readme[end_idx:]
    README_PATH.write_text(f'{before}\n\n{table_md}\n{after}', encoding='utf-8')


def write_csv(skills: list[dict], path: Path) -> None:
    fieldnames = [
        'name', 'slug', 'description', 'short_description', 'why', 'what', 'how', 'results',
        'version', 'updated', 'jtbd_1', 'jtbd_2', 'jtbd_3',
        'audit_kind', 'audit_author', 'audit_category', 'audit_trust_score', 'audit_last_audited',
        'audit_permission_file_read', 'audit_permission_file_write', 'audit_permission_network', 'audit_permission_shell',
        'path',
    ]
    with path.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(skills)


def main() -> int:
    skills = load_skills()
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    table_md = markdown_table(skills)
    (CATALOG_DIR / 'skills.md').write_text(table_md, encoding='utf-8')
    (CATALOG_DIR / 'skills.json').write_text(json.dumps(skills, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    write_csv(skills, CATALOG_DIR / 'skills.csv')
    update_readme(table_md)
    print(f'Catalog generated: {len(skills)} skills')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
