import logging
from typing import Self, Union, Tuple

from core.layout import Widget
from core.renderer import TextAlignment, RGBA
from core.text_template import TextTemplate
from core.utils import parse_color

logger = logging.getLogger(__name__)


class TextWidget(Widget):
    def __init__(self, template: str):
        super().__init__()
        # TODO: think about the naming
        self.content: str = template
        self.x: float = 0.0
        self.y: float = 0.0
        self.font_size = 20
        self.alignment: TextAlignment = TextAlignment.CENTER
        self.color: RGBA = (255, 255, 255, 255)

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

    def set_alignment(self, alignment: TextAlignment) -> Self:
        self.alignment = alignment
        return self

    def set_color(self, color: Union[RGBA, str, Tuple[int, int, int]]) -> Self:
        self.color = parse_color(color)
        return self

    def draw(self, renderer, variable_map):
        # Resolve the variables before rendering
        text = self._template.resolve(variable_map)

        # Render the text
        renderer.draw_text((self.x, self.y), text, color=self.color, align=self.alignment)


class ImageWidget(Widget):
    def __init__(self, source: str):
        super().__init__()
        self.source: str = source
        self.x: float = 0.0
        self.y: float = 0.0


class RectWidget(Widget):
    def __init__(self):
        super().__init__()
        self.x: float = 0.0
        self.y: float = 0.0
        self.width: float = 0.0
        self.height: float = 0.0
        self.color: RGBA = (255, 255, 255, 255)

    def set_x(self, x: float) -> Self:
        self.x = x
        return self

    def set_y(self, y: float) -> Self:
        self.y = y
        return self

    def set_width(self, width: float) -> Self:
        self.width = width
        return self

    def set_height(self, height: float) -> Self:
        self.height = height
        return self

    def set_color(self, color: Union[RGBA, str, Tuple[int, int, int]]) -> Self:
        self.color = parse_color(color)
        return self

    def draw(self, renderer, variable_map):
        renderer.draw_rect((self.x, self.y), (self.width, self.height), color=self.color, fill=True)
