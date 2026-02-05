import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = process.cwd();
const SKILLS_DIR = join(ROOT, 'skills');
const CATALOG_DIR = join(ROOT, 'catalog');
const README_PATH = join(ROOT, 'README.md');

function parseFrontmatter(content) {
	const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
	if (!match) return null;

	const yaml = match[1];
	const result = {};

	let currentKey = null;
	let nestedObj = null;

	for (const line of yaml.split('\n')) {
		if (!line.trim()) continue;

		if (/^\s{2,}\w/.test(line) && currentKey) {
			const nestedMatch = line.trim().match(/^(\w+):\s*(.+)$/);
			if (nestedMatch) {
				if (!nestedObj) nestedObj = {};
				let val = nestedMatch[2].trim();
				if (val === 'true') val = true;
				else if (val === 'false') val = false;
				nestedObj[nestedMatch[1]] = val;
			}
			continue;
		}

		if (currentKey && nestedObj) {
			result[currentKey] = nestedObj;
			nestedObj = null;
		}

		const topMatch = line.match(/^(\w+):\s*(.*)?$/);
		if (topMatch) {
			currentKey = topMatch[1];
			let val = (topMatch[2] || '').trim();

			if (val === '') {
				nestedObj = {};
				continue;
			}

			if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
				val = val.slice(1, -1);
			}

			if (val === 'true') val = true;
			else if (val === 'false') val = false;
			else if (/^\d+$/.test(val)) val = parseInt(val, 10);

			result[currentKey] = val;
			nestedObj = null;
		}
	}

	if (currentKey && nestedObj && Object.keys(nestedObj).length > 0) {
		result[currentKey] = nestedObj;
	}

	return result;
}

function permsToShort(perms) {
	const parts = [];
	if (perms?.fileRead === true) parts.push('R');
	if (perms?.fileWrite === true) parts.push('W');
	if (perms?.network === true) parts.push('Net');
	if (perms?.shell === true) parts.push('Sh');
	return parts.length ? parts.join(',') : '-';
}

function kindRank(kind) {
	if (kind === 'auditor') return 0;
	if (kind === 'module') return 1;
	return 2;
}

function loadSkills() {
	if (!existsSync(SKILLS_DIR)) throw new Error(`Missing skills dir: ${SKILLS_DIR}`);

	const dirs = readdirSync(SKILLS_DIR, { withFileTypes: true })
		.filter(d => d.isDirectory())
		.map(d => d.name)
		.sort((a, b) => a.localeCompare(b));

	const skills = [];
	for (const slug of dirs) {
		const skillPath = join(SKILLS_DIR, slug, 'SKILL.md');
		const raw = readFileSync(skillPath, 'utf-8');
		const fm = parseFrontmatter(raw);
		if (!fm?.name) continue;

		skills.push({
			name: fm.name,
			slug,
			version: fm.version || '',
			author: fm.author || '',
			description: fm.description || '',
			kind: fm.kind || '',
			category: fm.category || '',
			trustScore: typeof fm.trustScore === 'number' ? fm.trustScore : null,
			permissions: fm.permissions || {},
			lastAudited: fm.lastAudited || '',
			path: `skills/${slug}/SKILL.md`,
		});
	}

	skills.sort((a, b) => {
		const ak = kindRank(a.kind);
		const bk = kindRank(b.kind);
		if (bk != ak) return ak - bk;
		const at = a.trustScore ?? -1;
		const bt = b.trustScore ?? -1;
		if (bt !== at) return bt - at;
		return a.slug.localeCompare(b.slug);
	});

	return skills;
}

function toMarkdownTable(skills) {
	const header = [
		'| Skill | Type | Category | Trust | Perms | Last audited |',
		'| --- | --- | --- | ---: | --- | --- |',
	];

	const rows = skills.map(s => {
		const trust = s.trustScore ?? '';
		const perms = permsToShort(s.permissions);
		const audited = s.lastAudited || '';
		const kind = s.kind || '';
		const category = s.category || '';
		return `| [${s.slug}](${s.path}) | ${kind} | ${category} | ${trust} | ${perms} | ${audited} |`;
	});

	return header.concat(rows).join('\n') + '\n';
}

function updateReadmeTable(tableMd) {
	const readme = readFileSync(README_PATH, 'utf-8');
	const start = '<!-- catalog:start -->';
	const end = '<!-- catalog:end -->';

	const startIdx = readme.indexOf(start);
	const endIdx = readme.indexOf(end);
	if (startIdx === -1 || endIdx === -1 || endIdx < startIdx) {
		throw new Error('README.md is missing catalog markers');
	}

	const before = readme.slice(0, startIdx + start.length);
	const after = readme.slice(endIdx);
	const next = `${before}\n\n${tableMd}\n${after}`;

	writeFileSync(README_PATH, next);
}

function main() {
	const skills = loadSkills();
	const tableMd = toMarkdownTable(skills);

	mkdirSync(CATALOG_DIR, { recursive: true });
	writeFileSync(join(CATALOG_DIR, 'skills.md'), tableMd);
	writeFileSync(join(CATALOG_DIR, 'skills.json'), JSON.stringify(skills, null, 2) + '\n');

	updateReadmeTable(tableMd);

	console.log(`Catalog generated: ${skills.length} skills`);
}

main();
