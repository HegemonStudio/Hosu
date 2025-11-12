from core.config import ConfigSection


@ConfigSection(name="renderer_pillow")
class RendererPillowConfig:
    font_path: str = "resources/fonts/Roboto.ttf"

