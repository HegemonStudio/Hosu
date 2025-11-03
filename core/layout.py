from abc import ABC
from dataclasses import dataclass, field
from typing import List

from core.errors import NotImplementedWidgetError
from core.logger import get_logger
from core.namespaced_key import NamespacedKey

logger = get_logger(__name__)


class Widget(ABC):
    KEY: NamespacedKey = None

    def draw(self, renderer, variable_map):
        raise NotImplementedWidgetError(renderer.__class__.__name__, self.__class__.__name__)


@dataclass
class Layer:
    widgets: List[Widget] = field(default_factory=list)


@dataclass
class Layout:
    width: int
    height: int
    layers: List[Layer] = field(default_factory=list)
