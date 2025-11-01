from dataclasses import dataclass

import rosu_pp_py as rosu

from osu.replay import OsuReplay

@dataclass
class Performance:
    pp: float
    star_rating: float

def calculate(beatmap_path: str, replay: OsuReplay) -> Performance:
    perf = rosu.Performance(
        accuracy=replay.accuracy * 100,
        lazer=False,
        misses=replay.count_misses,
        combo=replay.greatest_combo,
        hitresult_priority=rosu.HitResultPriority.BestCase,
    )
    perf.set_mods(replay.mods)

    map = rosu.Beatmap(path=beatmap_path)
    max_attrs = perf.calculate(perf.calculate(map))

    p = Performance(pp=max_attrs.pp, star_rating=max_attrs.difficulty.stars)
    return p
