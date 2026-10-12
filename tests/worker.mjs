import assert from 'node:assert/strict';
import worker from '../dist/server/index.js';

const origin = 'https://example.test';
const page = await worker.fetch(new Request(origin + '/'));
assert.equal(page.status, 200);
const html = await page.text();
assert.match(html, /Analyze with AI/);
assert.doesNotMatch(html, /quick.?check/i);
const status = await worker.fetch(new Request(origin + '/api/status'));
assert.deepEqual((await status.json()).configured, false);
const unavailable = await worker.fetch(new Request(origin + '/api/analyze', { method: 'POST', body: '{}' }));
assert.match((await unavailable.json()).error, /locally/);
assert.equal((await worker.fetch(new Request(origin + '/style.css'))).status, 200);
console.log('Hosted preview smoke tests passed');
