"""Download the phishing classifier once; inference never calls Hugging Face."""
from pathlib import Path
from huggingface_hub import snapshot_download

repo = "specific-AI/email-agent-phishing-detection"
target = Path(__file__).resolve().parents[1] / "models" / "phishing-detector"
target.mkdir(parents=True, exist_ok=True)
snapshot_download(
    repo_id=repo,
    local_dir=str(target),
    allow_patterns=["config.json", "model.safetensors", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "vocab.txt"],
)
print(f"Model downloaded to {target}")
