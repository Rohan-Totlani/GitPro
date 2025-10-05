import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root if present
ROOT = Path(__file__).resolve().parent
env_path = ROOT / '.env'
if env_path.exists():
	load_dotenv(dotenv_path=env_path)

# Simple settings accessor. Values are read from environment variables.
GITHUB_APP_ID = os.environ.get("GITHUB_APP_ID")
GITHUB_APP_PRIVATE_KEY_PATH = os.environ.get("GITHUB_APP_PRIVATE_KEY_PATH")
GITHUB_APP_PRIVATE_KEY = os.environ.get("GITHUB_APP_PRIVATE_KEY")
GITHUB_WEBHOOK_SECRET = os.environ.get("GITHUB_WEBHOOK_SECRET")

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-mpnet-base-v2")

