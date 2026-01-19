import re
import subprocess

from src.models import Action
from src.llm import OpenAILLM


def execute_action(
    command: Action, provided_values: dict[str, str | None], api_key: str
) -> str:
    if not command.prompt:
        raise ValueError(f"Action '{command.name}' has no prompt defined")

    validated_params = {}
    missing_params = []

    for param in command.params:
        provided_value = provided_values.get(param.name)
        resolved_value = param.resolve_value(provided_value)

        if resolved_value is None:
            missing_params.append(param.name)
        else:
            validated_params[param.name] = resolved_value

    if missing_params:
        params_list = ", ".join(f"--{p}" for p in missing_params)
        raise ValueError(
            f"Missing required parameter(s) for action '{command.name}': {params_list}\n"
            f"Please provide values for all required parameters."
        )

    command_outputs = {}
    for cmd in command.commands:
        command_output = _execute_command(_fill_template(cmd.value, validated_params))
        command_outputs[cmd.name] = command_output

    response = OpenAILLM(api_key).generate(
        _fill_template(command.prompt, {**validated_params, **command_outputs})
    )

    if response is None:
        raise ValueError("LLM returned empty response")

    return response


### private ###


def _execute_command(command_str: str, cwd: str = ".") -> str:
    result = subprocess.run(
        command_str, shell=True, cwd=cwd, capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr}")

    return result.stdout


def _fill_template(template: str, params: dict[str, str]) -> str:
    result = template
    for key, value in params.items():
        result = result.replace(f"{{{{{key}}}}}", value)
    return result
