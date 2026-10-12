// ASSETS is injected by scripts/build.mjs. Hosted Site is a visual demo; AI runs locally.
// Model inference is available only in local/server.py on the owner's Mac.
const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' } });
export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === '/api/status') return json({ configured: false, model: null });
    if (url.pathname === '/api/analyze') return json({ error: 'Open SignalDesk locally to use the on-device model.' }, 503);
    if (request.method !== 'GET') return new Response('Method not allowed', { status: 405 });
    const asset = url.pathname === '/' ? ASSETS['/index.html'] : ASSETS[url.pathname];
    if (!asset) return new Response('Not found', { status: 404 });
    const type = url.pathname.endsWith('.css') ? 'text/css' : url.pathname.endsWith('.js') ? 'text/javascript' : 'text/html';
    return new Response(asset, { headers: { 'content-type': `${type}; charset=utf-8`, 'cache-control': 'public, max-age=300' } });
  },
};
