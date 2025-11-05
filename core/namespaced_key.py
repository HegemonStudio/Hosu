from typing import Self, Type

from core.logger import get_logger

logger = get_logger(__name__)


def is_valid_char(ch: str) -> bool:
    return ch.isalnum() or ch == '_'


class NamespacedKey:
    def __init__(self, namespace: str, key: str):
        """
        Creates a namespaced key.
        """
        self.namespace = namespace.lower()
        self.key = key.lower()
        self._validate()

    def _validate(self):
        # TODO: namespace and key cannot be empty.
        # Checking namespace
        for i in range(len(self.namespace)):
            ch = self.namespace[i]
            if not is_valid_char(ch):
                msg_error = (f"Key can only consist of alphanumeric characters and underscores.\n"
                             f"Invalid namespace character: '{ch}' at\n"
                             f"{self.namespace}:{self.key}\n"
                             f"{' ' * i}^")
                raise ValueError(msg_error)
        # Checking key
        for i in range(len(self.key)):
            ch = self.key[i]
            if not is_valid_char(ch):
                msg_error = (f"Key can only consist of alphanumeric characters and underscores.\n"
                             f"Invalid key character: '{ch}' at\n"
                             f"{self.namespace}:{self.key}\n"
                             f"{' ' * (len(self.namespace) + 1)}{' ' * i}^")
                raise ValueError(msg_error)

    def __str__(self):
        return f"{self.namespace}:{self.key}"

    def __eq__(self, other):
        if not isinstance(other, NamespacedKey):
            return False
        return self.namespace == other.namespace and self.key == other.key

    def __hash__(self):
        return hash((self.namespace, self.key))

    def __repr__(self):
        return f"{self.namespace}:{self.key}"

    @classmethod
    def from_string(cls: Type[Self], string: str) -> Self:
        # TODO: check is string a string type
        # TODO: use partition instead of split, cause split trims the spaces between "a:b d"
        args = string.split(":")
        if len(args) != 2:
            raise ValueError(f"Invalid namespaced key format. Expected 'namespace:key'.\n"
                             f" Got: '{string}'")
        return NamespacedKey(args[0], args[1])
