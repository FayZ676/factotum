from pydantic import BaseModel


class Param(BaseModel):
    name: str
    type: str
    default: str | None
    description: str | None

    def resolve_value(self, provided_value: str | None) -> str | None:
        if provided_value is not None:
            return provided_value
        return self.default

    def is_required(self) -> bool:
        return self.default is None


class Command(BaseModel):
    name: str
    value: str


class Action(BaseModel):
    name: str
    params: list[Param]
    commands: list[Command]
    prompt: str | None


class Config(BaseModel):
    openai_api_key: str
    actions: list[Action]
