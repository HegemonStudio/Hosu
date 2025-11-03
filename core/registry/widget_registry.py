from typing import List, Dict, Type, Self

from core.layout import Widget
from core.logger import get_logger
from core.namespaced_key import NamespacedKey

logger = get_logger(__name__)

# Decorator for registering widgets
def RegisterWidget(cls):
    if not issubclass(cls, Widget):
        raise TypeError(f"RegisterWidget decorator can only be applied to subclasses of Widget.")

    # the class must have a static KEY attribute of type NamespacedKey
    if not hasattr(cls, "KEY"):
        raise ValueError(f"Widget class {cls.__name__} must have an static 'KEY' attribute.")
    if cls.KEY is None:
        raise ValueError(f"Widget class {cls.__name__} has 'KEY' attribute set to None.")
    if not isinstance(cls.KEY, NamespacedKey):
        raise TypeError(f"Widget class {cls.__name__} has 'KEY' attribute that is not a NamespacedKey.")

    WidgetRegistry.register(cls.KEY, cls)

    return cls


class WidgetRegistry:
    _registry: Dict[NamespacedKey, Type[Widget]] = dict()

    @classmethod
    def get(cls: Type[Self], key: NamespacedKey | str) -> Type[Widget]:
        # Convert string key to NamespacedKey if necessary
        if isinstance(key, str):
            key = NamespacedKey.from_string(key)

        if not cls.is_registered(key):
            raise KeyError(f"Widget with key '{key}' is not registered.")

        return cls._registry[key]

    @classmethod
    def register(cls: Type[Self], key: NamespacedKey | str, widget_cls: Type[Widget]) -> None:
        # Convert string key to NamespacedKey if necessary
        if isinstance(key, str):
            key = NamespacedKey.from_string(key)
        if key is None:
            raise ValueError("Widget key cannot be None.")
        if cls.is_registered(key):
            raise KeyError(f"Widget with key '{key}' is already registered.")
        # Ensure the widget_class is a subclass of Widget
        if widget_cls is None:
            raise ValueError("Widget class cannot be None.")
        if not issubclass(widget_cls, Widget):
            raise TypeError(f"Registered object must be an instance of Widget.")

        # Register the widget
        cls._registry[key] = widget_cls

        logger.info(f"Registered widget with key '{key}'.")

    @classmethod
    def unregister(cls: Type[Self], key: NamespacedKey | str) -> None:
        # Convert string key to NamespacedKey if necessary
        if isinstance(key, str):
            key = NamespacedKey.from_string(key)

        if not cls.is_registered(key):
            # If the widget is not registered, log and skip
            logger.info(f"Widget with key '{key}' is not registered, cannot unregister.")
            return

        # Unregister the widget
        cls._registry.pop(key)

        logger.info(f"Unregistered widget with key '{key}'.")

    @classmethod
    def all(cls: Type[Self]):
        return cls._registry.items()

    @classmethod
    def is_registered(cls: Type[Self], key: NamespacedKey | str) -> bool:
        # Convert string key to NamespacedKey if necessary
        if isinstance(key, str):
            key = NamespacedKey.from_string(key)

        return key in cls._registry

