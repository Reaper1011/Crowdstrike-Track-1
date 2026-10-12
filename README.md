# SignalDesk — local phishing triage

SignalDesk is a SOC analyst demo that reviews pasted emails. A quick check runs in the browser; an optional phishing classifier runs **on your own Mac**. The model is [specific-AI/email-agent-phishing-detection](https://huggingface.co/specific-AI/email-agent-phishing-detection), a compact BERT email classifier from Hugging Face. Hugging Face is used only to download the model weights once. Email content is never sent to Hugging Face inference services.

## Run on this Mac

From this repository, with Python 3.10+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/download_model.py
.venv/bin/python local/server.py
```

Open **http://127.0.0.1:4173**. The server binds to loopback only. After the model download, classification runs offline. Model files stay in `models/` and are not committed. No Ollama or API token is needed.

The classifier returns a phishing/not-phishing signal and confidence. SignalDesk's browser checks separately highlight exact email text and suggest verification steps. The model does not generate or substantiate those explanations. Inputs longer than 512 model tokens are truncated for classification; the interface discloses this. Results are provisional and should be checked against trusted sender, URL, header, and attachment tools.

## Hosted preview

The [private SignalDesk Site](https://signaldesk-soc-triage.coraldream6.chatgpt.site/) shows the same interface and browser quick check. Its AI button is disabled because the model runs on your Mac only. The hosted code has no model API calls or Hugging Face token.

## Files

- `web/` — responsive interface and browser quick check
- `local/server.py` — local HTTP server and on-device classification
- `scripts/download_model.py` — one-time model weight download
- `worker/index.js` — hosted preview static assets only
- `scripts/build.mjs` — embeds browser assets for the private preview
- `tests/worker.mjs` — hosted preview smoke checks

Node.js is only needed to rebuild the hosted preview: `node scripts/build.mjs && node tests/worker.mjs`.
