"""Git utilities for GitScribe."""

import sys
import subprocess
import click


def run_git_command(cmd) -> str:
    """Execute a git command and handle errors."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stdout:
            return result.stdout.strip()
        else:
            return ""

    except subprocess.CalledProcessError as e:
        click.echo(f"Error running git command: {e.stderr.strip()}", err=True)
        sys.exit(1)
    except FileNotFoundError:
        click.echo(
            "Error: git command not found. Make sure git is installed and in your PATH.",
            err=True,
        )
        sys.exit(1)
