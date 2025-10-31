import logging

from core.errors import UnsupportedWidgetError
from core.layout import Widget

logger = logging.getLogger(__name__)

class TextWidget(Widget):
  def __init__(self, text: str):
    super().__init__()
    self.content = text

  def draw(self, renderer, variable_map):
    if hasattr(renderer, "draw_text"):
      renderer.draw_text(self, variable_map)
    else:
      raise UnsupportedWidgetError(renderer.__class__.__name__, self.__class__.__name__)

  content: str = ""
  x: float = 0.0
  y: float = 0.0

class ImageWidget(Widget):
  source: str = ""
  x: float = 0.0
  y: float = 0.0

