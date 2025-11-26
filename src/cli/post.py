import click
import pyperclip

from src.file_utils import get_default_style_path, get_style
from src.cli.utils import require_api_key
from src.llm import OpenAILLM
from src.prompts import post_prompt
from src.git_utils import run_git_command
from src.validators import validate_value_type, validate_date_string_format


def _save_content_to_file(content: str, file_path: str) -> None:
    """Save generated content to a file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def _build_git_log_command(last, since, until):
    """Build git log command with optional filters."""
    cmd = ["git", "log", "--oneline"]
    has_date_filter = since is not None or until is not None

    if since is not None and validate_date_string_format(
        value=since, accept_format="%Y-%m-%d"
    ):
        cmd.extend([f"--since={since}"])

    if until is not None and validate_date_string_format(
        value=until, accept_format="%Y-%m-%d"
    ):
        cmd.extend([f"--until={until}"])

    if (
        not has_date_filter
        and last is not None
        and validate_value_type(value=last, accept_type=int)
    ):
        cmd.extend(["-n", str(last)])

    return cmd


@click.command()
@click.option("--last", default=1, help="Number of commits to fetch (default: 1)")
@click.option("--since", default=None, help="Include commits since date (YYYY-MM-DD)")
@click.option("--until", default=None, help="Include commits until date (YYYY-MM-DD)")
@click.option(
    "--style",
    default=None,
    help="Style file for the LLM to reference when generating post content (optional)",
)
@click.option(
    "--output",
    default=None,
    help="Output file path to save generated content (default: gitscribe_output.txt)",
)
def post(last, since, until, style, output):
    """Generate post content from git commits."""
    cmd = _build_git_log_command(last, since, until)
    commits = run_git_command(cmd)

    style_file = style
    if not style_file:
        style_file = get_default_style_path("post")

    style_content = get_style(file_path=style_file)

    if not commits:
        click.echo("❌ No commits found matching the criteria.")
        return

    click.echo(f"💬 Commits:\n{commits}")
    api_key = require_api_key("OPENAI_API_KEY")
    response = OpenAILLM(api_key=api_key).generate(
        prompt=post_prompt.substitute(commits=commits, style=style_content)
    )

    if not response:
        click.echo("❌ Failed to generate content")
        return

    pyperclip.copy(response)
    click.echo(f"\n📝 Generated Content:\n{response}")
    click.echo("\n📋 Content copied to clipboard!")

    output_file = output if output else "gitscribe_output.txt"
    _save_content_to_file(response, output_file)
    click.echo(f"\n✅ Content saved to: {output_file}")
