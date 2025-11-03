import traceback
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Tuple

from core.layout import Layout, Layer
from core.logger import get_logger
from core.variable_map import VariableMap

logger = get_logger(__name__)


class TextAlignment(str, Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"


RGBA = Tuple[int, int, int, int]


# TODO: think about the renderer API, maybe it should be different
class Renderer(ABC):
    """
    Abstract base class for all renderers (Pillow etc.).
    Defines the API widgets can use to draw text or images.
    """

    @abstractmethod
    def begin(self, layout: Layout) -> None:
        """
        Initializes the renderer on the given layout.
        """
        pass

    @abstractmethod
    def end(self) -> Any:
        """
        Finalizes the renderer on the given layout.
        Returns the rendered image.
        """
        pass

    @abstractmethod
    def draw_text(self, position: Tuple[float, float], text: str, font_size: float = 0, color: RGBA = (255, 255, 255, 255),
                  align: TextAlignment = TextAlignment.LEFT, drop_shadow: bool = False) -> None:
        """
        Draws text on the given position.
        :param position: Position of the text to be drawn.
        :param text: Text to be drawn.
        :param color: Color of the text to be drawn.
        :param align: Alignment of the text to be drawn.
        """
        pass

    @abstractmethod
    def draw_rect(self, position: Tuple[float, float], size: Tuple[int, int], color: RGBA = (255, 255, 255, 255),
                  fill: bool = True) -> None:
        """
        Draws rectangle on the given position.

        :param position: Position of the rectangle to be drawn.
        :param size: Size of the rectangle to be drawn.
        :param color: Color of the rectangle to be drawn.
        :param fill: Whether to fill the rectangle or not.
        """
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
                print(traceback.format_exc())
