import json
from typing import Tuple, Union, Any

from core.logger import get_logger

logger = get_logger(__name__)


def dump_json(data: Any, filename: str) -> None:
    if data is None:
        return
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
        logger.info(f"Dumped json into: {filename}")


# TODO: create Color class
def parse_color(color: Union[str, Tuple[int, int, int], Tuple[int, int, int, int]]) -> list[int]:
    """Parse a hex color string (with optional # and alpha) into an (R, G, B, [A]) tuple."""
    if isinstance(color, str):
        color = color.strip().lstrip('#')
        length = len(color)

        if length == 3:  # #RGB
            r, g, b = [int(c * 2, 16) for c in color]
            return [r, g, b, 255]

        elif length == 4:  # #RGBA
            r, g, b, a = [int(c * 2, 16) for c in color]
            return [r, g, b, a]

        elif length == 6:  # #RRGGBB
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            return [r, g, b, 255]

        elif length == 8:  # #RRGGBBAA
            r = int(color[0:2], 16)
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            a = int(color[6:8], 16)
            return [r, g, b, a]

        else:
            raise ValueError(f"Invalid hex color format: {color}")

    elif isinstance(color, list):
        if len(color) in (3, 4):
            return list(int(c) for c in color)
        else:
            raise ValueError("Tuple color must be length 3 (RGB) or 4 (RGBA).")

    else:
        raise TypeError("Color must be a hex string or a tuple.")
