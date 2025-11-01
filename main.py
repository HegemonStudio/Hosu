import os

import dotenv

from core.layout import Layout, Layer
from core.logger import get_logger
from core.variable_map import VariableMap
from core.variables import TextVariable, NumberVariable, ImageURLVariable
from core.widgets import TextWidget, ImageWidget
from osu.api import OsuAPI
from osu.replay import OsuReplay
from renderer.pillow import PillowRenderer

logger = get_logger("Hosu")

def main():
    logger.info("Hello Hosu!")
    dotenv.load_dotenv()

    api = OsuAPI(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

    user = api.get_user("Gofrr")
    print(user.country_code)

    layout = Layout(800, 400, [
        Layer([
          TextWidget("Wynik: {SCORE}"),
          ImageWidget("{BACKGROUND}")
        ]),
    ])

    vars = VariableMap()
    vars.set("SCORE", NumberVariable(123))
    vars.set("PLAYER", TextVariable("Moderr"))
    vars.set("BACKGROUND", ImageURLVariable("https://xd.click/czeslaw.png"))

    renderer = PillowRenderer()
    img = renderer.render_layout(layout, vars)
    img.show()


if __name__ == "__main__":
    main()

