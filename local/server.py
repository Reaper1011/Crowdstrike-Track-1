"""Local-only SignalDesk web server and phishing classifier."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
MODEL_DIR = ROOT / "models" / "phishing-detector"
HOST = "127.0.0.1"
PORT = int(os.environ.get("SIGNALDESK_PORT", "4173"))
_model = None
_tokenizer = None


def load_model():
    global _model, _tokenizer
    if _model is None:
        from transformers import AutoModelForSequenceClassification, AutoTokenizer
        _tokenizer = AutoTokenizer.from_pretrained(str(MODEL_DIR), local_files_only=True)
        _model = AutoModelForSequenceClassification.from_pretrained(str(MODEL_DIR), local_files_only=True)
        _model.eval()
    return _model, _tokenizer


def classify(email):
    import torch
    model, tokenizer = load_model()
    inputs = tokenizer(email, return_tensors="pt", truncation=True, max_length=512)
    with torch.inference_mode():
        probs = torch.softmax(model(**inputs).logits, dim=-1)[0]
    index = int(probs.argmax())
    label = str(model.config.id2label[index])
    return {"phishing": label.lower() == "true", "confidence": round(float(probs[index]), 4), "model": "specific-AI/email-agent-phishing-detection", "truncated": len(tokenizer.encode(email, add_special_tokens=True)) > 512}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, data, status=200):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/api/status":
            ready = (MODEL_DIR / "model.safetensors").is_file()
            self.send_json({"configured": ready, "model": "Specific AI phishing detector" if ready else None})
            return
        assets = {"/": ("index.html", "text/html"), "/index.html": ("index.html", "text/html"), "/style.css": ("style.css", "text/css"), "/app.js": ("app.js", "text/javascript")}
        if path not in assets:
            self.send_error(404)
            return
        name, mime = assets[path]
        data = (WEB / name).read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime + "; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        origin = self.headers.get("Origin")
        if origin and origin not in (f"http://{HOST}:{PORT}", f"http://localhost:{PORT}"):
            self.send_json({"error": "Cross-origin requests are blocked."}, 403)
            return
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            self.send_json({"error": "JSON request required."}, 415)
            return
        if urlsplit(self.path).path != "/api/analyze":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 100_000:
                self.send_json({"error": "Request is too large."}, 413)
                return
            body = json.loads(self.rfile.read(size))
            email = body.get("email")
        except (ValueError, json.JSONDecodeError, AttributeError):
            self.send_json({"error": "Invalid request body."}, 400)
            return
        if not isinstance(email, str) or not email.strip() or len(email) > 20_000:
            self.send_json({"error": "Enter an email of up to 20,000 characters."}, 400)
            return
        if not (MODEL_DIR / "model.safetensors").is_file():
            self.send_json({"error": "Local model is missing. Run the download command in README.md."}, 503)
            return
        try:
            self.send_json(classify(email))
        except Exception as exc:
            print(f"Local classifier error: {exc}", flush=True)
            self.send_json({"error": "Local model failed. Check the server terminal."}, 500)


def main():
    print(f"SignalDesk on http://{HOST}:{PORT} (local only)", flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
