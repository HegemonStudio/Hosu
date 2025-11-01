import base64
import json
import os
import struct
from dataclasses import dataclass
from json import JSONEncoder
from typing import BinaryIO


def read_byte(file: BinaryIO) -> int:
    return struct.unpack('<B', file.read(1))[0]


def read_short(file: BinaryIO) -> int:
    return struct.unpack('<H', file.read(2))[0]


def read_int(file: BinaryIO) -> int:
    return struct.unpack('<I', file.read(4))[0]


def read_long(file: BinaryIO) -> int:
    return struct.unpack('<Q', file.read(8))[0]


def read_osustring(file: BinaryIO) -> str:
    """
    osu! string format has three parts.

    1. a single byte (marker) which wil be either
       0x00 (decimal  0) indicating that the next two parts are absent.
       0x0b (decimal 11) indicating that the next two parts are present.
    2. a ULEB128 representing the byte length of the following string
    3. the string itself, encoded in UTF-8.

    Reference:
    https://osu.ppy.sh/wiki/en/Client/File_formats/osr_%28file_format%29

    :param file: The file stream
    :return: The osu! string
    """
    marker = read_byte(file)
    if marker == 0x00:
        return ""
    if marker != 0x0B:
        raise ValueError("Invalid Osu! string marker (expected 0x0B or 0x00)")

    length = read_byte(file)
    return file.read(length).decode('utf-8')


class OsuReplay:
    def __init__(self, path: str):
        # Check does replay file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"OsuReplay: file '{path}' does not exists.")
        # Try to read and parse replay file
        try:
            with open(path, "rb") as replay:
                self.mode = self._read_mode(replay)
                self.osu_version = read_int(replay)
                self.beatmap_hash = read_osustring(replay)  # beatmap MD5 hash
                self.user_name = read_osustring(replay)
                self.replay_hash = read_osustring(replay)  # replay MD5 hash

                self.count_300 = read_short(replay)
                self.count_100 = read_short(replay)
                self.count_50 = read_short(replay)
                self.count_gekis = read_short(replay)
                self.count_katus = read_short(replay)
                self.count_misses = read_short(replay)
                self.accuracy = (self.count_50 * 50 + self.count_100 * 100 + self.count_300 * 300) / (300 * (self.count_50 + self.count_100 + self.count_300 + self.count_misses))
                self.total_score = read_int(replay)
                self.greatest_combo = read_short(replay)
                self.is_perfect = read_byte(replay)
                self.mods = read_int(replay)
                self.life_bar = read_osustring(replay)
                self.timestamp = read_long(replay)  # windows ticks

                data_length = read_int(replay)
                self.compressed_data = replay.read(data_length)
                # self.online_score_id = read_long(replay)
        except Exception as e:
            raise RuntimeError(f"OsuReplay: cannot open replay file: {e}")

    def _read_mode(self, replay) -> str:
        """
        Determines the mode of given replay
        """
        mode: int = read_byte(replay)
        return {
            0: 'osu!',
            1: 'osu!taiko',
            2: 'osu!catch',
            3: 'osu!mania',
        }.get(mode, 'unknown')


    def toJSON(self):
        return {
            "mode": self.mode,
            "osu_version": self.osu_version,
            "beatmap_hash": self.beatmap_hash,
            "user_name": self.user_name,
            "replay_hash": self.replay_hash,
            "count_300": self.count_300,
            "count_100": self.count_100,
            "count_50": self.count_50,
            "count_gekis": self.count_gekis,
            "count_katus": self.count_katus,
            "count_misses": self.count_misses,
            "accuracy": self.accuracy,
            "total_score": self.total_score,
            "greatest_combo": self.greatest_combo,
            "is_perfect": self.is_perfect,
            "mods": self.mods,
            "life_bar": self.life_bar,
            "timestamp": self.timestamp,
            "compressed_data": base64.b64encode(self.compressed_data).decode("utf-8"),
        }

