import click
import pyperclip

from src.file_utils import get_default_style_path, get_style
from src.cli.utils import require_api_key
from src.llm import OpenAILLM
from src.prompts import commit_prompt
from src.git_utils import run_git_command


@click.command()
@click.option(
    "--style",
    default=None,
    help="Style file for the LLM to reference when generating commit messages (optional)",
)
def commit(style):
    """Generate a commit message from git diff."""
    diff = run_git_command(["git", "diff", "--cached"])

    if not diff:
        click.echo(
            "❌ No staged changes found. Stage your changes with 'git add' first."
        )
        return

    click.echo("📊 Analyzing changes...")

    style_file = style
    if not style_file:
        style_file = get_default_style_path("commit")

    style_content = get_style(file_path=style_file)
    api_key = require_api_key("OPENAI_API_KEY")
    response = OpenAILLM(api_key=api_key).generate(
        prompt=commit_prompt.substitute(diff=diff, style=style_content)
    )

    if not response:
        click.echo("❌ Failed to generate content")
        return

    pyperclip.copy(response)
    click.echo(f"\n✅ Generated Commit Message:\n{response}")
    click.echo("\n📋 Commit message copied to clipboard!")

    if click.confirm("\n💬 Do you want to commit these changes with this message?"):
        run_git_command(["git", "commit", "-m", response])
        click.echo("✅ Changes committed successfully!")
    else:
        click.echo("⏭️  Commit skipped. You can commit manually later.")
