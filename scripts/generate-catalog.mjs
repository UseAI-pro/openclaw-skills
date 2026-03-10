import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const script = join(__dirname, 'generate_catalog.py');
const result = spawnSync('python3', [script], { stdio: 'inherit' });
if (result.error) throw result.error;
process.exit(result.status ?? 1);
