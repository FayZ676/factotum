from pathlib import Path

import click

from src.file_utils import (
    save_config,
    load_config,
    CONFIG_FILE,
)


def _set_default_style_path(style_type: str, file_path: str) -> None:
    """Save default style file path to config."""
    config = load_config()
    key = f"default_{style_type}_style"
    config[key] = file_path
    save_config(config)


def _ensure_style_file_exists(file_path: str) -> None:
    """Create an empty style file if it doesn't exist."""
    if not file_path:
        return

    path = Path(file_path)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()


def _save_api_key(api_key: str, key_name: str) -> None:
    """Save API key to config file with user feedback."""
    config = load_config()
    config[key_name] = api_key
    save_config(config)
    click.echo(f"✅ API key saved to {CONFIG_FILE}")


def _prompt_for_openai_api_key() -> str:
    """Interactively prompt user for API key."""
    click.echo("\n🔑 OpenAI API Key Required")
    click.echo("\nYou can get your API key from: https://platform.openai.com/api-keys")
    click.echo("\nYou have two options for storing your API key:")
    click.echo("  1. Store in config file (this command)")
    click.echo("  2. Set the OPENAI_API_KEY environment variable")
    click.echo(
        "\nThis command will store the key securely in your home directory (~/.gitscribe/config.json)"
    )

    api_key = click.prompt("\nEnter your OpenAI API key", hide_input=True)
    return api_key.strip()


def _prompt_for_style_file(style_type: str) -> str:
    """Interactively prompt user for style file path."""
    click.echo(f"\n📄 Default {style_type.capitalize()} Style File")
    click.echo(f"\nSpecify the path to your default {style_type} style file.")
    click.echo(
        f"This file will be used when you run 'gitscribe {style_type}' without the --style option."
    )
    click.echo("If the file doesn't exist, GitScribe will create it as an empty file.")

    file_path = click.prompt(
        f"\nEnter the path to your default {style_type} style file",
        default="",
        show_default=False,
    )
    return file_path.strip()


@click.command()
def configure():
    """Configure GitScribe settings (API keys, etc.)."""
    api_key = _prompt_for_openai_api_key()
    _save_api_key(api_key=api_key, key_name="OPENAI_API_KEY")

    commit_style_path = _prompt_for_style_file("commit")
    if commit_style_path:
        was_created = not Path(commit_style_path).exists()
        _ensure_style_file_exists(commit_style_path)
        if was_created:
            click.echo(f"✅ Created empty style file: {commit_style_path}")
        _set_default_style_path("commit", commit_style_path)
        click.echo(f"✅ Default commit style file set to: {commit_style_path}")

    post_style_path = _prompt_for_style_file("post")
    if post_style_path:
        was_created = not Path(post_style_path).exists()
        _ensure_style_file_exists(post_style_path)
        if was_created:
            click.echo(f"✅ Created empty style file: {post_style_path}")
        _set_default_style_path("post", post_style_path)
        click.echo(f"✅ Default post style file set to: {post_style_path}")

    click.echo(
        "\n✅ Configuration complete! You can now use the commands `gitscribe post` and `gitscribe commit`."
    )
