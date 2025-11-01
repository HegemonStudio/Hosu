import logging
from typing import Self, Union, Tuple

from core.layout import Widget
from core.renderer import TextAlignment, RGBA
from core.text_template import TextTemplate
from core.utils import parse_color

logger = logging.getLogger(__name__)


class TextWidget(Widget):
    def __init__(self, template: str = ""):
        super().__init__()
        # TODO: think about the naming
        self.content: str = template
        self.x: float = 0.0
        self.y: float = 0.0
        self.font_size = 1
        self.alignment: TextAlignment = TextAlignment.CENTER
        self.color: RGBA = (255, 255, 255, 255)
        self.drop_shadow: bool = False

        self._template = TextTemplate(template)

    def set_text(self, text: str) -> Self:
        self.content = text
        self._template = TextTemplate(text)
        return self

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
        logger.info(f"Color = {self.color}")
        return self

    def please_drop_shadow(self):
        self.drop_shadow = True
        return self

    def draw(self, renderer, variable_map):
        # Resolve the variables before rendering
        text = self._template.resolve(variable_map)

        # Render the text
        c = (int(self.color[0]), int(self.color[1]), int(self.color[2]), int(self.color[3]))
        renderer.draw_text((self.x, self.y), text, color=c, align=self.alignment, font_size=self.font_size, drop_shadow=self.drop_shadow)


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
        self.width: float = 1.0
        self.height: float = 1.0
        self.color = [255, 255, 255, 255]

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
        logger.info(f"Color = {self.color}")
        return self

    def draw(self, renderer, variable_map):
        c = (int(self.color[0]), int(self.color[1]), int(self.color[2]), int(self.color[3]))
        renderer.draw_rect((self.x, self.y), (self.width, self.height), color=c, fill=True)

    def set_opacity(self, param: float) -> Self:
        self.color[3] = int(255 * param)
        return self
