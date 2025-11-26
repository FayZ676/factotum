"""CLI commands for GitScribe."""

import click

from src.cli.configure import configure
from src.cli.post import post
from src.cli.commit import commit


@click.group()
def gitscribe():
    """GitScribe - Transform your git history into shareable content."""


# Register commands
gitscribe.add_command(configure)
gitscribe.add_command(post)
gitscribe.add_command(commit)


__all__ = ["configure", "post", "commit", "gitscribe"]
