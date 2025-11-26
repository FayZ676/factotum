import click

from src.file_utils import get_api_key


def require_api_key(key_name: str) -> str:
    """Get API key or raise error if not found."""
    api_key = get_api_key(key_name)
    if not api_key:
        click.echo(f"❌ No {key_name} found!", err=True)
        click.echo("\nYou can either:", err=True)
        click.echo("  1. Run: gitscribe configure", err=True)
        click.echo(f"  2. Set the {key_name} environment variable", err=True)
        raise click.Abort()
    return api_key
