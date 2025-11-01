from typing import Tuple, Any

from PIL import Image, ImageDraw, ImageFont

from core.layout import Layout
from core.logger import get_logger
from core.renderer import Renderer, RGBA, TextAlignment

logger = get_logger(__name__)

BACKGROUND_COLOR = (0, 0, 0, 255)


class PillowRenderer(Renderer):
    def draw_text(self, position: Tuple[float, float], text: str, font: Any = None, color: RGBA = (255, 255, 255, 255),
                  align: TextAlignment = TextAlignment.LEFT) -> None:
        font = ImageFont.truetype("resources/fonts/Roboto.ttf", 30)

        x = self.layout.width * position[0]
        y = self.layout.height * position[1]

        # Get text size
        text_width = self.draw.textlength(text, font=font)

        match align:
            case TextAlignment.RIGHT:
                x -= text_width
            case TextAlignment.CENTER:
                x -= text_width / 2
            case _:
                pass

        self.draw.text((x, y), text, font=font, fill=color)

    def draw_rect(self, position: Tuple[float, float], size: Tuple[int, int], color: RGBA = (255, 255, 255, 255),
                  fill: bool = True) -> None:
        self.draw.rectangle((position[0], position[1], position[0] + size[0], position[1] + size[1]), fill=color)

    def __init__(self):
        self.image: Image.Image | None = None
        self.draw: ImageDraw.ImageDraw | None = None
        self.layout: Layout | None = None

    def begin(self, layout: Layout) -> None:
        logger.info("PillowRenderer begin")
        self.layout = layout
        self.image = Image.new("RGBA", (layout.width, layout.height), BACKGROUND_COLOR)
        self.draw = ImageDraw.Draw(self.image)

    # def draw_text(self, text: str = "", midpoint_x: float = 0.0, midpoint_y: float = 0.0) -> None:
    #     x = self.layout.width * midpoint_x
    #     y = self.layout.height * midpoint_y
    #     self.draw.text((x, y), text)

    def end(self) -> Image.Image:
        logger.info("PillowRenderer end")
        return self.image
