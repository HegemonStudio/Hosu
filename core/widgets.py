import logging

from typing import Self

from core.errors import UnsupportedWidgetError
from core.layout import Widget
from core.text_template import TextTemplate

logger = logging.getLogger(__name__)


class TextWidget(Widget):
    def __init__(self, template: str):
        super().__init__()
        # TODO: think about the naming
        self.content: str = template
        self.x: float = 0.0
        self.y: float = 0.0
        self.font_size = 20

        self._template = TextTemplate(template)

    def set_x(self, x: float) -> Self:
        self.x = x
        return self

    def set_y(self, y: float) -> Self:
        self.y = y
        return self

    def set_font_size(self, font_size) -> Self:
        self.font_size = font_size
        return self

    def draw(self, renderer, variable_map):
        if hasattr(renderer, "draw_text"):
            # Resolve the variables before rendering
            text = self._template.resolve(variable_map)

            # Render the text
            renderer.draw_text(text, self.x, self.y)
        else:
            raise UnsupportedWidgetError(renderer.__class__.__name__, self.__class__.__name__)


class ImageWidget(Widget):
    def __init__(self, source: str):
        super().__init__()
        self.source: str = source
        self.x: float = 0.0
        self.y: float = 0.0

