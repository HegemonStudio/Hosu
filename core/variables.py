from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any

from core.logger import get_logger

logger = get_logger(__name__)


# TODO: move type to inside Variable
class VariableType(Enum):
    TEXT = auto()
    NUMBER = auto()
    IMAGE_URL = auto()


# TODO: add Generic Variable[T]
class Variable(ABC):
    def __init__(self, variable_type: VariableType):
        self.variable_type = variable_type

    def is_type(self, t: VariableType) -> bool:
        return self.variable_type == t

    @abstractmethod
    def get_value(self) -> Any:  # TODO: type hint with Generic
        pass

    @abstractmethod
    def get_text(self) -> str:
        pass

    # TODO: __eq__ and __hash__ methods


class TextVariable(Variable):
    def __init__(self, text: str):
        # TODO: enforce str type, e.g. convert numbers to str?s
        super().__init__(VariableType.TEXT)
        self.text = text

    def get_text(self) -> str:
        return self.text

    def get_value(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"TextVariable(\"{self.text}\")"


class NumberVariable(Variable):
    def __init__(self, number: float):
        super().__init__(VariableType.NUMBER)
        self.number: float = number

    def get_value(self) -> float:
        return self.number

    def get_text(self) -> str:
        return f"{self.number}"

    def __repr__(self) -> str:
        return f"NumberVariable({self.number})"


class ImageURLVariable(Variable):
    def __init__(self, url: str):
        super().__init__(VariableType.IMAGE_URL)
        self.url = url

    def get_value(self) -> str:
        return self.url

    def get_text(self) -> str:
        return self.url

    def __repr__(self) -> str:
        return f"ImageURLVariable(url=\"{self.url}\")"
