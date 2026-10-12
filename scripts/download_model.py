"""Download Qwen weights once; inference is entirely local afterward."""
from pathlib import Path
from huggingface_hub import snapshot_download

REPO = "mlx-community/Qwen3-4B-Instruct-2507-4bit"
TARGET = Path(__file__).resolve().parents[1] / "models" / "qwen-email"
TARGET.mkdir(parents=True, exist_ok=True)
snapshot_download(repo_id=REPO, local_dir=str(TARGET))
print(f"Qwen model downloaded to {TARGET}")
