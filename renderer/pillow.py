from typing import Tuple, Any

from PIL import Image, ImageDraw, ImageFont

from core.layout import Layout
from core.logger import get_logger
from core.renderer import Renderer, RGBA, TextAlignment

logger = get_logger(__name__)

BACKGROUND_COLOR = (0, 0, 0, 255)


class PillowRenderer(Renderer):
    def draw_text(self, position: Tuple[float, float], text: str, font_size: float = 1.0, color: RGBA = (255, 255, 255, 255),
                  align: TextAlignment = TextAlignment.LEFT, drop_shadow: bool = False) -> None:
        # TODO: remove hardcoded font path
        font = ImageFont.truetype("resources/fonts/Roboto.ttf", self.layout.width / 16 * font_size)

        x = self.layout.width * position[0]
        y = self.layout.height * position[1]

        # Get text size
        # TODO: replace with bbox method for better accuracy and height calculation
        text_width = self.draw.textlength(text, font=font)

        match align:
            case TextAlignment.RIGHT:
                x -= text_width
            case TextAlignment.CENTER:
                x -= text_width / 2
            case _:
                pass

        if drop_shadow:
            self.draw_text((position[0] + 0.002, position[1] + 0.002), text, font_size=font_size, color=(0,0,0,255), align=align, drop_shadow=False)

        self.draw.text((x, y), text, font=font, fill=color)

    def draw_rect(self, position: Tuple[float, float], size: Tuple[int, int], color: RGBA = (255, 255, 255, 255),
                  fill: bool = True) -> None:
        x = self.layout.width * position[0]
        y = self.layout.height * position[1]
        w = self.layout.width * size[0]
        h = self.layout.height * size[1]
        self.draw.rectangle(((x, y), (x + w, y + h)), fill=color)

    def __init__(self):
        self.image: Image.Image | None = None
        self.draw: ImageDraw.ImageDraw | None = None
        self.layout: Layout | None = None

    def begin(self, layout: Layout) -> None:
        logger.info("PillowRenderer begin")
        self.layout = layout
        self.image = Image.new("RGBA", (layout.width, layout.height), BACKGROUND_COLOR)
        self.draw = ImageDraw.Draw(self.image)

    def end(self) -> Image.Image:
        logger.info("PillowRenderer end")
        return self.image
