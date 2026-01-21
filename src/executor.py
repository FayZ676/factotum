import subprocess

from rich.panel import Panel
from rich.prompt import Confirm
from rich.console import Console

from src.llm import OpenAILLM
from src.models import Action, Step


def execute_action(
    action: Action,
    args: dict[str, str | None],
    llm: OpenAILLM,
    console: Console,
    status=None,
) -> str | None:
    step_outputs = {}
    validated_params = _validate_and_collect_params(action.steps, args)

    for step in action.steps:
        resolved_value = _fill_template(step.value, {**validated_params}, step_outputs)

        if step.confirm:
            if not _prompt_step_confirmation(step, console, status):
                continue

        # TODO: Switch case?
        if step.type == "shell":
            output = _execute_shell(resolved_value)
            step_outputs[step.name] = output
        elif step.type == "llm":
            output = llm.generate(resolved_value)
            if output is None:
                raise ValueError(f"LLM returned empty response for step '{step.name}'")
            step_outputs[step.name] = output
        else:
            raise ValueError(f"Unknown step type: {step.type}")

    if not action.steps:
        raise ValueError(f"Action '{action.name}' has no steps defined")

    for step in reversed(action.steps):
        if step.name in step_outputs:
            return step_outputs[step.name]

    return None


### private ###


def _prompt_step_confirmation(step: Step, console: Console, status=None) -> bool:
    if status:
        status.stop()

    console.print(
        f"\n[bold cyan]Step:[/bold cyan] [bold]{step.name}[/bold]: {step.description}"
    )
    confirmed = Confirm.ask("[bold]Execute this step?[/bold]", default=True)

    if not confirmed:
        console.print(f"[dim]⊗ Skipped '{step.name}'[/dim]")

    if status:
        status.start()

    return confirmed


def _execute_shell(command_str: str, cwd: str = ".") -> str:
    result = subprocess.run(
        command_str, shell=True, cwd=cwd, capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr}")

    return result.stdout


def _fill_template(
    template: str, params: dict[str, str], step_outputs: dict[str, str]
) -> str:
    result = template

    for step_name, output in step_outputs.items():
        result = result.replace(f"{{{{@{step_name}}}}}", output)

    for key, value in params.items():
        result = result.replace(f"{{{{{key}}}}}", value)

    return result


def _validate_and_collect_params(
    steps: list[Step], provided_values: dict[str, str | None]
) -> dict[str, str]:
    all_params = {}
    missing_params = []

    for step in steps:
        for param in step.params:
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
