# SignalDesk — local CyberSecQwen email triage

SignalDesk is a SOC analyst demo for suspicious email review. A quick evidence check runs in the browser. **CyberSecQwen-4B**, a cybersecurity fine-tune based on Qwen3-4B-Instruct-2507, runs locally on an Apple silicon Mac through llama.cpp. It produces a provisional priority, plain-English summary, quoted evidence, and safe next steps.

The model is distributed as a 4-bit GGUF file by [mradermacher](https://huggingface.co/mradermacher/CyberSecQwen-4B-GGUF), a community quantization of [athena129/CyberSecQwen-4B](https://huggingface.co/athena129/CyberSecQwen-4B). The original model targets cybersecurity threat-intelligence questions and CVE/CWE mapping, not phishing email specifically, so email triage quality should be treated as experimental. Hugging Face is used only to download model weights once. Email text is not sent to Hugging Face or another hosted inference service. No Ollama or API token is used.

## Run on this Mac

Requires Apple silicon, macOS 14+, and a native Python 3.10+. The llama.cpp Python package compiles locally during install and may take several minutes.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/download_model.py
.venv/bin/python local/server.py
```

Open **http://127.0.0.1:4173**. The web server binds to loopback only. The model file is stored in `models/` and is excluded from GitHub.

The app displays model findings only when their quotes exactly match the supplied email. The AI report includes a 0–100% model-estimated phishing-risk indicator and a separate quick-check score. The percentage is not a calibrated probability or confidence score. Priority follows the model score bands (low 0–34, medium 35–69, high 70–100); when the independent browser quick check assigns a higher priority, SignalDesk shows the higher combined priority and reports both scores. Neither path verifies live links, attachments, sender reputation, or authentication results. Analysts should check those with trusted tools before disposition.

## Hosted preview

The [private SignalDesk Site](https://signaldesk-soc-triage.coraldream6.chatgpt.site/) shows the same interface and browser quick check. Its AI button is disabled because the model runs on your Mac only. The hosted code contains no model API calls or Hugging Face token.

## Files

- `web/` — interface and browser quick check
- `local/server.py` — loopback server and local CyberSecQwen inference
- `scripts/download_model.py` — one-time cybersecurity model download
- `worker/index.js` — hosted preview static assets only
- `scripts/build.mjs` — embeds browser assets for the private preview
- `tests/worker.mjs` — hosted preview smoke checks

Node.js is only needed to rebuild the hosted preview: `node scripts/build.mjs && node tests/worker.mjs`.
