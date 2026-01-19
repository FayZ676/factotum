import subprocess

from src.llm import OpenAILLM
from src.models import Action, Command


def execute_action(
    action: Action, provided_values: dict[str, str | None], api_key: str
) -> str:
    # TODO: Prompt is optional, this shouldn't matter.
    if not action.prompt:
        raise ValueError(f"Action '{action.name}' has no prompt defined")

    validated_params = _validate_and_collect_params(action.commands, provided_values)
    command_outputs = {}
    for cmd in action.commands:
        cmd_params = {param.name: validated_params[param.name] for param in cmd.params}
        command_output = _execute_command(_fill_template(cmd.value, cmd_params))
        command_outputs[cmd.name] = command_output

    response = OpenAILLM(api_key).generate(
        _fill_template(action.prompt, command_outputs)
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


def _validate_and_collect_params(
    commands: list[Command], provided_values: dict[str, str | None]
) -> dict[str, str]:
    all_params = {}
    missing_params = []

    for cmd in commands:
        for param in cmd.params:
            if param.name not in all_params:
                all_params[param.name] = param

    validated_params = {}
    for param_name, param in all_params.items():
        provided_value = provided_values.get(param_name)
        resolved_value = param.resolve_value(provided_value)

        if resolved_value is None:
            missing_params.append(param_name)
        else:
            validated_params[param_name] = resolved_value

    if missing_params:
        params_list = ", ".join(f"--{p}" for p in missing_params)
        raise ValueError(
            f"Missing required parameter(s): {params_list}\n"
            f"Please provide values for all required parameters."
        )

    return validated_params
