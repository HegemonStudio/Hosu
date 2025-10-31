from PIL import Image, ImageDraw

from core.layout import Layout
from core.logger import get_logger
from core.renderer import Renderer
from core.variable_map import VariableMap
from core.widgets import TextWidget

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

  def draw_text(self, widget: TextWidget, vars: VariableMap):
    x = widget.x * self.layout.width
    y = widget.y * self.layout.height
    self.draw.text((x, y), widget.content)

  def end(self) -> Image.Image:
    logger.info("PillowRenderer end")
    return self.image