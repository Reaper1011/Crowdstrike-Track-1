# SignalDesk — security analysis workspace

SignalDesk demonstrates three SOC analyst workflows with one local model: phishing email triage, security alert summaries, and plain-English explanations of malware behavior. **CyberSecQwen-4B**, a cybersecurity fine-tune based on Qwen3-4B-Instruct-2507, runs locally on an Apple silicon Mac through llama.cpp. Each report includes a provisional concern score, a concise summary, quoted evidence, unknowns, and safe next steps.

The model is distributed as a 4-bit GGUF file by [mradermacher](https://huggingface.co/mradermacher/CyberSecQwen-4B-GGUF), a community quantization of [athena129/CyberSecQwen-4B](https://huggingface.co/athena129/CyberSecQwen-4B). The model targets cybersecurity threat-intelligence questions and CVE/CWE mapping; these three workflows are prompt-based demonstrations, not separately trained or validated classifiers. Treat each estimate as experimental decision support. Model weights are downloaded from Hugging Face once; inference runs on the local workstation.

## Run locally

Requires Apple silicon, macOS 14+, and a native Python 3.10+. The llama.cpp Python package compiles locally during install and may take several minutes.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/download_model.py
.venv/bin/python local/server.py
```

Open **http://127.0.0.1:4173**. The web server binds to loopback only. The model file is stored in `models/` and is excluded from GitHub.

The app only displays findings whose quotes exactly match the supplied text. The 0–100 score is a model-estimated concern rating, not a calibrated probability or confidence score. Priority bands are low 0–34, medium 35–69, and high 70–100. The model does not inspect live links, execute files, query threat intelligence, or correlate external events. Analysts should validate findings with trusted tools.

## Alert sample source

The alert examples are sanitized excerpts from the [AIT Alert Data Set (AIT-ADS), Zenodo record 8263181](https://zenodo.org/records/8263181), Russell Mitchell scenario. They cover a web-shell-labeled Apache request, a UID change during the privilege-escalation phase, and a routine ClamAV update. The original dataset contains synthetic alerts from AMiner, Wazuh, and Suricata, along with attack-phase labels and false positives. The 96 MB archive is not bundled with this app. Malware examples are clearly labeled synthetic sandbox notes because the AIT-ADS is an alert dataset, not a malware-sample corpus.

## Files

- `web/` — analysis interface
- `local/server.py` — loopback server and task-specific local model prompts
- `scripts/download_model.py` — one-time cybersecurity model download
- `worker/index.js` — hosted preview static assets only
- `scripts/build.mjs` — embeds browser assets for the private preview
- `tests/worker.mjs` — hosted preview smoke checks

Node.js is only needed to rebuild the hosted preview: `node scripts/build.mjs && node tests/worker.mjs`.
