import json
from pathlib import Path

from src.models import Action, Command, Param


CONFIG_DIR = Path.home() / ".gitscribe"
CONFIG_FILE = CONFIG_DIR / "config.json"


def get_config_path() -> Path:
    """Get the path to the config file."""
    return CONFIG_FILE


def load_config() -> dict:
    """Load configuration from ~/.gitscribe/config.json"""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config file not found at {CONFIG_FILE}. "
            f"Please run 'gitscribe init' to create it."
        )

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def get_api_key() -> str:
    """Get OpenAI API key from config."""
    config = load_config()
    api_key = config.get("openai_api_key")
    if not api_key:
        raise ValueError(
            "OpenAI API key not found in config. Please run 'gitscribe init'."
        )
    return api_key


def get_actions() -> list[Action]:
    """Get all actions from config as Command objects."""
    config = load_config()
    actions = config.get("actions", [])

    commands = []
    for action in actions:
        commands_list = [Command(**cmd) for cmd in action.get("commands", [])]
        commands.append(
            Action(
                name=action["name"],
                params=[Param(**param) for param in action.get("params", [])],
                commands=commands_list,
                prompt=action.get("prompt"),
            )
        )

    return commands


def save_config(config: dict):
    """Save configuration to file."""
    _ensure_config_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


### private ###


def _ensure_config_dir():
    """Ensure the config directory exists."""
    CONFIG_DIR.mkdir(exist_ok=True)
