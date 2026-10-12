import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const assets = {};
for (const name of ['index.html', 'style.css', 'app.js']) {
  assets[`/${name}`] = await readFile(resolve(root, 'web', name), 'utf8');
}
const source = await readFile(resolve(root, 'worker/index.js'), 'utf8');
await rm(resolve(root, 'dist'), { recursive: true, force: true });
await mkdir(resolve(root, 'dist/server'), { recursive: true });
await mkdir(resolve(root, 'dist/.openai'), { recursive: true });
await writeFile(resolve(root, 'dist/server/index.js'), `const ASSETS = ${JSON.stringify(assets)};\n${source}`);
await writeFile(resolve(root, 'dist/.openai/hosting.json'), await readFile(resolve(root, '.openai/hosting.json')));
console.log('Built Site worker');
