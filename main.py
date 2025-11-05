import os

import dotenv
from PIL import Image

from core.layout import Layout, Layer
from core.logger import get_logger
from core.utils import dump_json
from core.variable_map import VariableMap
from core.variables import TextVariable, NumberVariable, ImageURLVariable
from core.widgets import WidgetRect
from osu.api import OsuAPI
from osu.calculate import calculate_play_performance
from osu.replay import OsuReplay
from renderer.pillow import PillowRenderer

logger = get_logger("Hosu")


def main():
    logger.info("Hello Hosu!")
    # TODO: .env is so annoying, switch to config file later
    # TODO: generate config.toml
    dotenv.load_dotenv()

    vars = VariableMap()
    vars.set("SCORE", NumberVariable(123))
    vars.set("PLAYER", TextVariable("Moderr"))
    vars.set("BACKGROUND", ImageURLVariable("https://xd.click/czeslaw.png"))

    # TODO: use data from config file
    api = OsuAPI(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

    # TODO: use replay from run arguments
    # TODO: add example/replay.osr
    replay = OsuReplay("data/replay.osr")
    dump_json(replay.toJSON(), 'data/replay.json')
    user = api.get_user(replay.user_name)
    dump_json(user.json, 'data/user.json')
    beatmap = api.lookup_beatmap(replay.beatmap_hash)
    dump_json(beatmap.json, 'data/beatmap.json')

    # TODO: cache beatmap files storage/
    osu_file = api.download_beatmap(beatmap.id)
    with open("data/beatmap.osu", "w", encoding="utf-8") as f:
        f.write(osu_file)

    performance = calculate_play_performance("data/beatmap.osu", replay)
    vars.set("PP", TextVariable(f"{performance.pp:.0f}"))
    vars.set("STARS", TextVariable(f"{performance.star_rating:.2f}"))

    layout = Layout(1920, 1080, [
        Layer([
            # TODO: remove the repetitive set_
            WidgetRect().set_color("#07090C").set_width(1).set_height(1),
            WidgetRect().set_color("#0A0F16").set_x(0.5).set_y(0.06).set_width(1).set_height(0.12),
            WidgetRect().set_color("#0B121A").set_x(0.5).set_y(0.15).set_width(1).set_height(0.10),
            WidgetRect().set_color("#0C151E").set_x(0.5).set_y(0.23).set_width(1).set_height(0.10),
            WidgetRect().set_color("#0E1923").set_x(0.5).set_y(0.31).set_width(1).set_height(0.10),
            WidgetRect().set_color("#101E29").set_x(0.5).set_y(0.39).set_width(1).set_height(0.10),
            WidgetRect().set_color("#122330").set_x(0.5).set_y(0.47).set_width(1).set_height(0.10),
            WidgetRect().set_color("#152A3A").set_x(0.5).set_y(0.55).set_width(1).set_height(0.10)
        ]),
    ])

    # TODO: for later we should use RendererFactory to create renderers
    # RendererFactory.create_renderer("pillow")
    renderer = PillowRenderer()
    img: Image.Image = renderer.render_layout(layout, vars)
    img.show()
    img.save("data/benger.png")


if __name__ == "__main__":
    main()
