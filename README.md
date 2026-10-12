# SignalDesk — local Qwen email triage

SignalDesk is a SOC analyst demo for suspicious email review. A quick evidence check runs in the browser. **Qwen3-4B-Instruct-2507** runs locally on an Apple silicon Mac through Apple's MLX runtime and produces a provisional priority, plain-English summary, exact quoted evidence, and safe next steps.

The downloadable [4-bit MLX model](https://huggingface.co/mlx-community/Qwen3-4B-Instruct-2507-4bit) is a conversion of [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507). Hugging Face is used only to download weights once. Email text is not sent to Hugging Face or any other hosted inference service. No Ollama or API token is needed.

## Run on this Mac

From this repository, with Apple silicon, macOS 14+, and a native Python 3.10+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/download_model.py
.venv/bin/python local/server.py
```

Open **http://127.0.0.1:4173**. The server binds to loopback only. After the download, inference is offline. Model files stay in `models/` and are not committed to GitHub.

Qwen's findings are displayed only when their quotes exactly match the supplied email. The app also offers independent browser pattern checks. Neither path verifies live links, attachments, sender reputation, or authentication results. Analysts should verify those with trusted tools before disposition.

## Hosted preview

The [private SignalDesk Site](https://signaldesk-soc-triage.coraldream6.chatgpt.site/) shows the same interface and browser quick check. Its Qwen button is disabled because the model runs on your Mac only. The hosted code contains no model API calls or Hugging Face token.

## Files

- `web/` — interface and browser quick check
- `local/server.py` — loopback server and local Qwen inference
- `scripts/download_model.py` — one-time Qwen weight download
- `worker/index.js` — hosted preview static assets only
- `scripts/build.mjs` — embeds browser assets for the private preview
- `tests/worker.mjs` — hosted preview smoke checks

Node.js is only needed to rebuild the hosted preview: `node scripts/build.mjs && node tests/worker.mjs`.
