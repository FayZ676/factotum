import re
import subprocess

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
    if not action.steps:
        raise ValueError(f"Action '{action.name}' has no steps defined")

    step_outputs = {}
    skipped_steps = set()
    validated_params = _validate_and_collect_params(action.steps, args)

    for step in action.steps:
        dependencies = _extract_step_dependencies(step.value)
        blocked_by = dependencies & skipped_steps

        if blocked_by:
            console.print(
                f"[dim]⊗ Skipping '{step.name}' (depends on skipped: "
                f"{', '.join(blocked_by)})[/dim]"
            )
            skipped_steps.add(step.name)
            continue

        if step.confirm and not _prompt_step_confirmation(step, console, status):
            skipped_steps.add(step.name)
            continue

        resolved_value = _fill_template(step.value, validated_params, step_outputs)
        try:
            step_outputs[step.name] = _execute_step(step, resolved_value, llm)
        except Exception as e:
            console.print(f"[red]✗ Step '{step.name}' failed: {e}[/red]")
            raise

    for step in reversed(action.steps):
        if step.name in step_outputs:
            return step_outputs[step.name]
    return None


### private ###


def _execute_step(step: Step, resolved_value: str, llm: OpenAILLM) -> str:
    match step.type:
        case "shell":
            return _execute_shell(resolved_value)
        case "llm":
            output = llm.generate(resolved_value)
            if output is None:
                raise ValueError(f"LLM returned empty response for step '{step.name}'")
            return output
        case _:
            raise ValueError(f"Unknown step type: {step.type}")


def _extract_step_dependencies(template: str) -> set[str]:
    """Extract step names that this template depends on ({{@step_name}})."""
    return set(re.findall(r"\{\{@(\w+)\}\}", template))


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
