from PIL import Image, ImageDraw

from core.layout import Layout
from core.logger import get_logger
from core.renderer import Renderer

logger = get_logger(__name__)

BACKGROUND_COLOR = (0, 0, 0, 255)


class PillowRenderer(Renderer):
    def __init__(self):
        self.image: Image.Image | None = None
        self.draw: ImageDraw.ImageDraw | None = None
        self.layout: Layout | None = None

    def begin(self, layout: Layout) -> None:
        logger.info("PillowRenderer begin")
        self.layout = layout
        self.image = Image.new("RGBA", (layout.width, layout.height), BACKGROUND_COLOR)
        self.draw = ImageDraw.Draw(self.image)

    def draw_text(self, text: str = "", midpoint_x: float = 0.0, midpoint_y: float = 0.0):
        x = self.layout.width * midpoint_x
        y = self.layout.height * midpoint_y
        self.draw.text((x, y), text)

    def end(self) -> Image.Image:
        logger.info("PillowRenderer end")
        return self.image
