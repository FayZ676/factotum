"""Validation utilities for GitScribe."""

from datetime import datetime
from typing import TypeVar, Type, Optional
import click

T = TypeVar("T")


def validate_value_type(value: object, accept_type: Type[T]) -> Optional[T]:
    """Validates that a value is of the expected type, returning the value if valid or None if invalid."""
    if not isinstance(value, accept_type):
        click.echo("Error: Foo")
        return None
    return value


def validate_date_string_format(value: str, accept_format: str):
    """Validates that a date string matches the specified format and returns the value if valid, otherwise None."""
    try:
        datetime.strptime(value, accept_format)
        return value
    except ValueError:
        click.echo(
            f"Error: Value '{value}' does not match expected format '{accept_format}'"
        )
        return None
