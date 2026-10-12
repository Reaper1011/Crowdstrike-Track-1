import assert from 'node:assert/strict';
import worker from '../dist/server/index.js';

const origin = 'https://example.test';
const page = await worker.fetch(new Request(origin + '/'), {});
assert.equal(page.status, 200);
assert.match(await page.text(), /Analyze with Hugging Face AI/);
const status = await worker.fetch(new Request(origin + '/api/status'), {});
assert.deepEqual((await status.json()).configured, false);
const missing = await worker.fetch(new Request(origin + '/api/analyze', { method: 'POST', body: '{}' }), {});
assert.equal(missing.status, 503);

const email = 'From: Security <team@example.test>\nSubject: Urgent login verification';
const oldFetch = globalThis.fetch;
globalThis.fetch = async (_url, options) => {
  assert.equal(options.headers.authorization, 'Bearer test-token');
  return new Response(JSON.stringify({ choices: [{ message: { content: JSON.stringify({ priority: 'medium', summary: 'Verify the request.', findings: [{ title: 'Time pressure', quote: 'Urgent login verification', why: 'The subject urges action.' }, { title: 'Fabricated', quote: 'not in message', why: 'Should be removed.' }], unknowns: 'Sender authenticity is unknown.' }) } }] }), { status: 200 });
};
try {
  const result = await worker.fetch(new Request(origin + '/api/analyze', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ email }) }), { HF_TOKEN: 'test-token' });
  assert.equal(result.status, 200);
  const data = await result.json();
  assert.equal(data.level, 'Medium');
  assert.equal(data.findings.length, 1);
  assert.equal(data.findings[0].quote, 'Urgent login verification');
} finally { globalThis.fetch = oldFetch; }

console.log('Worker smoke tests passed');
