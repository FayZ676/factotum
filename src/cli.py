import sys
import json
import click
from pathlib import Path

from src.llm import OpenAILLM
from src.models import Action
from src.executor import execute_action
from src.config import save_config, load_config, get_api_key, CONFIG_FILE


@click.group()
def cli():
    """GitScribe - Transform your git history into content."""
    pass


@cli.command()
def init():
    """Initialize GitScribe configuration."""
    click.echo("Setting up GitScribe configuration...")
    api_key = click.prompt("Enter your OpenAI API key", hide_input=True)

    repo_config_path = Path(__file__).parent.parent / "config.json"
    if not repo_config_path.exists():
        click.echo(f"❌ Template config not found at {repo_config_path}", err=True)
        sys.exit(1)

    with open(repo_config_path, "r") as f:
        config = json.load(f)

    config["openai_api_key"] = api_key

    save_config(config)
    click.echo(f"✅ Configuration saved to {CONFIG_FILE}")
    click.echo("\nYou can now:")
    click.echo("  1. Edit the config file to add custom actions")
    click.echo("  2. Run 'gitscribe <action-name>' to execute actions")


def create_dynamic_cli():
    """
    Create a CLI with dynamically loaded commands from config.
    This is called at runtime to build the command structure.
    """
    try:
        actions = load_config().actions
    except (FileNotFoundError, ValueError):
        return cli

    for action in actions:

        def make_command(action: Action):
            @click.command(name=action.name, help=action.description)
            def dynamic_command(**kwargs):
                try:
                    result = execute_action(action, kwargs, OpenAILLM(get_api_key()))
                    click.echo(result)
                except Exception as e:
                    click.echo(f"❌ Error: {e}", err=True)
                    sys.exit(1)

            seen_params = {}
            for step in action.steps:
                for param in step.params:
                    if param.name not in seen_params:
                        seen_params[param.name] = param

            for param in seen_params.values():
                dynamic_command = click.option(
                    f"--{param.name}",
                    default=param.default,
                    help=param.description,
                    type=str if param.type == "string" else str,
                )(dynamic_command)

            return dynamic_command

        cli.add_command(make_command(action))

    return cli


def main():
    """Entry point for the CLI."""
    dynamic_cli = create_dynamic_cli()
    dynamic_cli()


if __name__ == "__main__":
    main()
