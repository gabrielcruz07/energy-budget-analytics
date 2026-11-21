import os
from pathlib import Path
from dotenv import load_dotenv

def get_project_root(marker: str = "README.md") -> Path:
    current_dir = Path(__file__).resolve().parent
    for parent in [current_dir] + list(current_dir.parents):
        if(parent / marker).exists():
            return parent
    raise FileNotFoundError(f"Project root marker '{marker}' not found.")

PROJECT_ROOT = get_project_root()
DATA_DIR = PROJECT_ROOT / "data"

load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

API_URL = os.getenv("API_URL","http://127.0.0.1:8000")

