import logging

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

        self._template = TextTemplate(template)

    def draw(self, renderer, variable_map):
        if hasattr(renderer, "draw_text"):
            # Resolve the variables before rendering
            text = self._template.resolve(variable_map)

            # Render the text
            renderer.draw_text(text)
        else:
            raise UnsupportedWidgetError(renderer.__class__.__name__, self.__class__.__name__)


class ImageWidget(Widget):
    def __init__(self, source: str):
        super().__init__()
        self.source: str = source
        self.x: float = 0.0
        self.y: float = 0.0

