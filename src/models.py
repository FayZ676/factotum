from typing import Literal

from pydantic import BaseModel


class Base(BaseModel):
    name: str
    description: str


class Param(Base):
    type: str
    default: str | None

    def resolve_value(self, provided_value: str | None) -> str | None:
        if provided_value is not None:
            return provided_value
        return self.default

    def is_required(self) -> bool:
        return self.default is None


class Step(Base):
    type: Literal["shell", "llm"]
    params: list[Param]
    value: str
    confirm: bool = False


class Action(Base):
    steps: list[Step]


class Config(BaseModel):
    openai_api_key: str
    actions: list[Action]
