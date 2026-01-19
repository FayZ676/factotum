import json
from pathlib import Path

from src.models import Config


CONFIG_DIR = Path.home() / ".factotum"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> Config:
    """Load configuration from ~/.factotum/config.json"""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config file not found at {CONFIG_FILE}. " f"Please run 'fac init'."
        )

    with open(CONFIG_FILE, "r") as f:
        return Config.model_validate_json(f.read())


def get_api_key() -> str:
    """Get OpenAI API key from config."""
    config = load_config()
    if not config.openai_api_key:
        raise ValueError("OpenAI API key not found in config. Please run 'fac init'.")
    return config.openai_api_key


def save_config(config: dict):
    """Save configuration to file."""
    _ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


### private ###


def _ensure_config_dir():
    """Ensure the config directory exists."""
    CONFIG_DIR.mkdir(exist_ok=True)
