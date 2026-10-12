"""Download the quantized CyberSecQwen weights; inference runs on this Mac."""
from pathlib import Path
from huggingface_hub import hf_hub_download

REPO = "mradermacher/CyberSecQwen-4B-GGUF"
FILENAME = "CyberSecQwen-4B.Q4_K_M.gguf"
TARGET = Path(__file__).resolve().parents[1] / "models" / "cybersecqwen-4b"
TARGET.mkdir(parents=True, exist_ok=True)
path = hf_hub_download(repo_id=REPO, filename=FILENAME, local_dir=str(TARGET))
print(f"CyberSecQwen model downloaded to {path}")
