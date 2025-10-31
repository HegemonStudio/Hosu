class HosuError(Exception):
  """ Base class for all Hosu errors """
  pass


class RendererError(HosuError):
  """ Base class for all renderer errors """
  pass


class UnsupportedWidgetError(RendererError):
  """ Raised when a widget is not supported """

  def __init__(self, renderer_name: str, widget_name: str):
    self.renderer_name = renderer_name
    self.widget_name = widget_name
    super().__init__(f"{renderer_name} is not supporting widget {widget_name}.")


class NotImplementedWidgetError(RendererError):
  """ Raised when a widget is not implemented """

  def __init__(self, renderer_name: str, widget_name: str):
    self.renderer_name = renderer_name
    self.widget_name = widget_name
    super().__init__(f"The {widget_name} has not implemented draw function and tried to render using {renderer_name}.")
