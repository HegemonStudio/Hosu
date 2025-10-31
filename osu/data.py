from typing import Any


class User:
    """
    osu! user object containing user data
    """

    def __init__(self, user_data: Any):
        self.user_data = user_data

        self.avatar_url = self._data("avatar_url")
        self.country_code = self._data("country_code")
        self.id = self._data("id")
        self.username = self._data("username")

    def _data(self, key: str, default: Any = None):
        """
        :param key: key in user json file
        :param default: default value if key not in user json file
        :return: json value with given key
        """
        if key not in self.user_data:
            if default is not None:
                return default
            # There is no key in data and no default.
            raise ValueError(f"Not found {key} in user data.")

        return self.user_data[key]
