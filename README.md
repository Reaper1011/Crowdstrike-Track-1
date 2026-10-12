# SignalDesk — phishing triage demo

A small, browser-based demo for **Track 1: AI for SOC Analyst**. Paste an email or choose one of three sample messages to get a provisional triage priority, quoted evidence, and recommended verification steps.

**Live demo:** https://signaldesk-soc-triage.coraldream6.chatgpt.site/

## Run locally

No installation, account, or API key is needed. From the repository root:

```sh
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000` in a browser. You can also open `dist/index.html` directly.

## What the demo does

- Checks sender and reply-to domains, links, time pressure, financial or credential requests, verification avoidance, and attachment cues.
- Shows exact excerpts from the supplied email for each finding.
- Offers a report to copy into a case note and an AI review prompt to paste into a model of your choice.
- Runs entirely in the browser. The page does not upload or store the pasted email.

The built-in priority is a **local heuristic**, not a model prediction or a final verdict. It cannot inspect attachments, full mail headers, URL redirects, domain reputation, or authentication results. An analyst should verify any consequential finding with trusted tools and procedures.

## Files

- `dist/index.html` — interface
- `dist/style.css` — responsive styling
- `dist/app.js` — sample emails, local analyzer, report and prompt generation
- `.openai/hosting.json` — configuration for the private Sites demo

## AI integration

The **Copy AI review prompt** button produces a prompt that treats email content as untrusted input and asks a model to cite exact evidence and state what it cannot determine. The demo does not call an AI API. To add live model analysis, use a server-side endpoint and keep the API credential in a server-side secret; do not put it in `dist/app.js` or browser storage.
