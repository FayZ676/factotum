"""File I/O utilities for GitScribe."""

import json
import os
from pathlib import Path

import click


CONFIG_DIR = Path.home() / ".gitscribe"
CONFIG_FILE = CONFIG_DIR / "config.json"


def _get_config_dir() -> Path:
    """Get the config directory, creating it if it doesn't exist."""
    CONFIG_DIR.mkdir(exist_ok=True)
    return CONFIG_DIR


def load_config() -> dict:
    """Load configuration from file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config: dict) -> None:
    """Save configuration to file."""
    _get_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_api_key(key_name: str) -> str | None:
    """Get API key from environment variable or config file."""
    api_key = os.environ.get(key_name)
    if api_key:
        return api_key

    config = load_config()
    return config.get(key_name)


def get_default_style_path(style_type: str) -> str | None:
    """Get the default style file path for a given style type (commit or post)."""
    config = load_config()
    key = f"default_{style_type}_style"
    return config.get(key)


def get_style(file_path: str | None) -> str:
    """Get style content from file. Returns empty string if no file provided or file doesn't exist."""
    if not file_path:
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        click.echo(f"⚠️  Style file '{file_path}' not found.", err=True)
        return ""
