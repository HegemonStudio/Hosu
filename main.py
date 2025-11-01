import os

import dotenv
import rosu_pp_py as rosu
from PIL.ImageEnhance import Color

from core.layout import Layout, Layer
from core.logger import get_logger
from core.renderer import TextAlignment
from core.utils import dump_json
from core.variable_map import VariableMap
from core.variables import TextVariable, NumberVariable, ImageURLVariable
from core.widgets import TextWidget, ImageWidget, RectWidget
from osu.api import OsuAPI
from osu.calculate import calculate
from osu.replay import OsuReplay
from renderer.pillow import PillowRenderer
logger = get_logger("Hosu")


def main():
    logger.info("Hello Hosu!")
    dotenv.load_dotenv()

    vars = VariableMap()
    vars.set("SCORE", NumberVariable(123))
    vars.set("PLAYER", TextVariable("Moderr"))
    vars.set("BACKGROUND", ImageURLVariable("https://xd.click/czeslaw.png"))

    api = OsuAPI(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

    replay = OsuReplay("old/replay2.osr")
    dump_json(replay.toJSON(), 'data/replay.json')
    user = api.get_user(replay.user_name)
    dump_json(user.json, 'data/user.json')
    beatmap = api.lookup_beatmap(replay.beatmap_hash)
    dump_json(beatmap.json, 'data/beatmap.json')

    osu_file = api.download_beatmap(beatmap.id)
    with open("data/beatmap.osu", "w", encoding="utf-8") as f:
        f.write(osu_file)


    performance = calculate("data/beatmap.osu", replay)
    logger.info("Star rating: %.2f", performance.star_rating)
    logger.info("PP: %.2f", performance.pp)

    vars.set("PP", TextVariable(f"{performance.pp:.0f}"))
    vars.set("STARS", TextVariable(f"{performance.star_rating:.2f}"))

    layout = Layout(1920, 1080, [
        Layer([
            RectWidget().set_color("#07090C").set_width(1).set_height(1),
            RectWidget().set_color("#0A0F16").set_x(0.5).set_y(0.06).set_width(1).set_height(0.12),
            RectWidget().set_color("#0B121A").set_x(0.5).set_y(0.15).set_width(1).set_height(0.10),
            RectWidget().set_color("#0C151E").set_x(0.5).set_y(0.23).set_width(1).set_height(0.10),
            RectWidget().set_color("#0E1923").set_x(0.5).set_y(0.31).set_width(1).set_height(0.10),
            RectWidget().set_color("#101E29").set_x(0.5).set_y(0.39).set_width(1).set_height(0.10),
            RectWidget().set_color("#122330").set_x(0.5).set_y(0.47).set_width(1).set_height(0.10),
            RectWidget().set_color("#152A3A").set_x(0.5).set_y(0.55).set_width(1).set_height(0.10)
        ]),
    ])

    renderer = PillowRenderer()
    img = renderer.render_layout(layout, vars)
    img.show()
    img.save("data/benger.png")


if __name__ == "__main__":
    main()
