import json
import os

import dotenv

from osu.replay import OsuReplay
from core.layout import Layout, Layer
from core.logger import get_logger
from core.variable_map import VariableMap
from core.variables import TextVariable, NumberVariable, ImageURLVariable
from core.widgets import TextWidget, ImageWidget
from osu.api import OsuAPI
from renderer.pillow import PillowRenderer
logger = get_logger("Hosu")


def main():
  logger.info("Hello Hosu!")
  dotenv.load_dotenv()



  api = OsuAPI(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

  replay = OsuReplay("old/replay3.osr")
  user = api.get_user(replay.user_name)
  print(replay.mode)
  print(user.country_code)

  layout = Layout(800, 400, [
    # Layer([
    #   TextWidget(text="Wynik: {SCORE}"),
    #   ImageWidget()
    # ]),
    Layer([
      TextWidget(text=f"Mode: {replay.mode}")
    ])
  ])

  vars = VariableMap()
  for field in replay.__dict__:
    if field.startswith('_'):
      continue
    vars.set(f"replay_{field}", TextVariable(f"{replay.__dict__[field]}"))
  for field in user.__dict__:
    if field.startswith('_'):
      continue
    vars.set(f"user_{field}", TextVariable(f"{user.__dict__[field]}"))

  vars.set("SCORE", NumberVariable(123))
  vars.set("PLAYER", TextVariable("Moderr"))
  vars.set("BACKGROUND", ImageURLVariable("https://xd.click/czeslaw.png"))

  renderer = PillowRenderer()
  img = renderer.render_layout(layout, vars)
  img.show()


if __name__ == "__main__":
  main()
