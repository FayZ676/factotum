import sys
import json
from pathlib import Path

import click
import pyperclip
from rich.panel import Panel
from rich.console import Console

from src.llm import OpenAILLM
from src.models import Action
from src.executor import execute_action
from src.config import save_config, load_config, get_api_key, CONFIG_FILE


console = Console()


@click.group()
def cli():
    """GitScribe - Transform your git history into content."""
    pass


@cli.command()
def init():
    """Initialize GitScribe configuration."""
    console.print("[bold cyan]Setting up GitScribe configuration...[/bold cyan]")
    api_key = click.prompt("Enter your OpenAI API key", hide_input=True)

    repo_config_path = Path(__file__).parent.parent / "config.json"
    if not repo_config_path.exists():
        console.print(f"[red]❌ Template config not found at {repo_config_path}[/red]")
        sys.exit(1)

    with open(repo_config_path, "r") as f:
        config = json.load(f)

    config["openai_api_key"] = api_key

    save_config(config)
    console.print(f"[green]✅ Configuration saved to {CONFIG_FILE}[/green]")
    console.print("\n[bold]You can now:[/bold]")
    console.print("  [cyan]1.[/cyan] Edit the config file to add custom actions")
    console.print(
        "  [cyan]2.[/cyan] Run [yellow]'gitscribe <action-name>'[/yellow] to execute actions"
    )


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
                    with console.status(
                        f"[bold cyan]Executing {action.name}...", spinner="dots"
                    ):
                        result = execute_action(
                            action, kwargs, OpenAILLM(get_api_key())
                        )
                    pyperclip.copy(result)
                    console.print(f"[bold]{result}[/bold]")
                    console.print("[dim]✓ Copied to clipboard[/dim]")
                except Exception as e:
                    console.print(
                        Panel(
                            f"[red]{str(e)}[/red]",
                            title="❌ Error",
                            border_style="red",
                            padding=(1, 2),
                        )
                    )
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
