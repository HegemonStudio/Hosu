import struct
from typing import BinaryIO


def read_byte(file: BinaryIO) -> int:
  return struct.unpack('B', file.read(1))[0]


def read_short(file: BinaryIO) -> int:
  return struct.unpack('H', file.read(2))[0]


def read_int(file: BinaryIO) -> int:
  return struct.unpack('I', file.read(4))[0]


def read_long(file: BinaryIO) -> int:
  return struct.unpack('Q', file.read(8))[0]

def read_osustring(file: BinaryIO) -> str:
  """
  osu! string has three parts.

  1. a single byte (marker) which wil be either
     0x00 (decimal  0) indicating that the next two parts are absent.
     0x0b (decimal 11) indicating that the next two parts are present.
  2. a ULEB128 representing the byte length of the following string
  3. the string itself, encoded in UTF-8.

  https://osu.ppy.sh/wiki/en/Client/File_formats/osr_%28file_format%29

  :param file: The file stream
  :return: The osu! string
  """
  marker = read_byte(file)
  if marker == 0x00:
    return ""
  if marker != 0x0B:
    raise RuntimeError("Invalid Osu! marker")

  length = read_byte(file)
  return file.read(length).decode('utf-8')


class OsuReplay:
  def __init__(self, path: str):
    try:
      with open(path, "rb") as replay:
        self._replay = replay

        self._read_mode()
        self.osu_version = read_int(replay)
        self.beatmap_hash = read_osustring(replay) # beatmap MD5 hash
        self.user_name = read_osustring(replay)
        self.replay_hash = read_osustring(replay) # replay MD5 hash

        self.count_300 = read_short(replay)
        self.count_100 = read_short(replay)
        self.count_50 = read_short(replay)
        self.count_gekis = read_short(replay)
        self.count_katus = read_short(replay)
        self.count_misses = read_short(replay)
        self.total_score = read_int(replay)
        self.greatest_combo = read_short(replay)
        self.is_perfect = read_byte(replay)
        self.mods = read_int(replay)
        self.life_bar = read_osustring(replay)
        self.timestamp = read_long(replay) # windows ticks

        data_length = read_int(replay)
        self.compressed_data = replay.read(data_length)
        # self.online_score_id = read_long(replay)

        self._replay = None
    except FileNotFoundError:
      raise RuntimeError("Cannot open replay file")

  def _read_mode(self) -> None:
    """
    determines the mode of given replay
    """
    mode: int = read_byte(self._replay)
    self.mode = {
      0: 'osu!',
      1: 'osu!taiko',
      2: 'osu!catch',
      3: 'osu!mania',
    }.get(mode, 'unknown')
