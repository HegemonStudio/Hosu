from abc import ABC, abstractmethod
from typing import Any

from core.layout import Layout, Layer
from core.logger import get_logger
from core.variable_map import VariableMap

logger = get_logger(__name__)


class Renderer(ABC):
    @abstractmethod
    def begin(self, layout: Layout) -> None:
        pass

    @abstractmethod
    def end(self) -> Any:
        pass

    def render_layout(self, layout: Layout, variable_map: VariableMap):
        self.begin(layout)
        for layer in layout.layers:
            self.render_layer(layer, variable_map)
        return self.end()

    def render_layer(self, layer: Layer, variable_map: VariableMap):
        logger.debug("Rendering layer")
        for widget in layer.widgets:
            try:
                widget.draw(self, variable_map)
            except Exception as e:
                logger.error(f"Encountered error while rendering widget {widget.__class__.__name__}: {e}")
