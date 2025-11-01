from typing import Any

class JsonData:
    """
    Base class for osu! json data objects
    """

    def __init__(self, json: Any):
        self.json = json

    def _data(self, key: str, default: Any = None) -> Any:
        """
        :param key: key in json file
        :param default: default value if key not in json file
        :return: json value with given key
        """
        if key not in self.json:
            if default is not None:
                return default
            # There is no key in data and no default.
            raise ValueError(f"Not found {key} in data.")

        return self.json[key]

"""
osu! data objects
"""

class User(JsonData):
    """
    osu! user object containing user data
    """

    def __init__(self, json: Any):
        super().__init__(json)

        self.avatar_url: str = self._data("avatar_url")
        self.country_code: str = self._data("country_code")
        self.id: int = self._data("id")
        self.username: str = self._data("username")


class Beatmap(JsonData):
    def __init__(self, json: Any):
        super().__init__(json)

        self.id: int = self._data("id")
        self.difficulty_rating: float = self._data("difficulty_rating")



