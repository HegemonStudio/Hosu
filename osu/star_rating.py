from enum import Enum


class StarRating(int, Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    INSANE = 4
    EXPERT = 5
    EXPERT_PLUS = 6
