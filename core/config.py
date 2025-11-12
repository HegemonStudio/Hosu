from dataclasses import dataclass
from pathlib import Path
from typing import Type, TypeVar, Callable, Any, TYPE_CHECKING, Generic

import tomlkit
from tomlkit import document, table

from core.logger import get_logger

logger = get_logger("hosu")

TF = TypeVar("TF")

@dataclass
class ConfigField(Generic[TF]):
    """
    Represents a configuration field with a name and a default value.
    """
    default: TF
    comment: str | None = None

if TYPE_CHECKING:
    def field(*, default: TF, comment: str | None = None) -> TF: ...
else:
    def field(*, default: TF, comment: str | None = None) -> ConfigField[TF]:
        """
        Helper function to create a ConfigField.

        Args:
            default: The default value of the configuration field.
            comment: An optional comment for the configuration field.

        Returns:
            A ConfigField instance.
        """
        return ConfigField(default=default, comment=comment)

class BaseConfigSection:
    """
    Base class for configuration sections.
    """
    NAME: str = "default"


    @classmethod
    def to_dict(cls) -> dict[str, object]:
        result = dict()
        exclude_field = lambda key, value: key.startswith("_") or key.startswith("__") or callable(
            value) or key == "NAME"

        for key, value in vars(cls).items():
            if exclude_field(key, value):
                continue
            if isinstance(value, ConfigField):
                result[key] = value.default
            else:
                result[key] = value

        return result

    @classmethod
    def comments(cls) -> dict[str, str]:
        result = dict()
        exclude_field = lambda key, value: key.startswith("_") or key.startswith("__") or callable(
            value) or key == "NAME"

        for key, value in vars(cls).items():
            if exclude_field(key, value):
                continue
            if isinstance(value, ConfigField) and value.comment is not None:
                result[key] = value.comment

        return result

known_sections: dict[str, Type[BaseConfigSection]] = dict()


def generate_config(path: Path):
    # Creates a new TOML document
    config_doc = document()

    # Iterates over all known sections
    for section_name, section_cls in known_sections.items():
        # Creates a new section table
        section_table = table()

        comments = section_cls.comments()

        # Add all fields from the section
        for key, value in section_cls.to_dict().items():
            it = tomlkit.item(value)
            if key in comments:
                it.comment(comments[key])

            section_table.add(key, it)

        # Add the section to the document
        config_doc.add(section_name, section_table)

    # Ensures the parent directory exists.
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write the config to file
    with open(path, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(config_doc))

    logger.info(f"Generated config file at: {path}")

T = TypeVar("T", bound=BaseConfigSection)
def ConfigSection(name: str) -> Callable[[type[T]], type[T]]:
    """
    Decorator to register a config section class.

    Args:
        name: The name of the config section.

    Returns:
        The decorator function.
    """
    def decorator(cls: type[T]) -> type[T]:
        if not issubclass(cls, BaseConfigSection):
            raise TypeError(f"ConfigSection decorator can only be applied to subclasses of BaseConfigSection.")
        cls.NAME = name
        known_sections[name] = cls
        return cls

    return decorator


def load_config(path: Path):
    if not path.exists():
        logger.warning(f"Missing config, generating default at: {path}")
        generate_config(path)

    with open(path, "rb") as f:
        data = tomlkit.load(f)

    modified = False

    for section_name, section_cls in known_sections.items():
        section = data.get(section_name)
        if section is None:
            # Section is missing
            logger.warning(f"Missing section [{section_name}], adding defaults.")

            # Create new section with default values
            t = tomlkit.table()
            for key, value in section_cls.to_dict().items():
                t.add(key, value)
            data.add(section_name, t)

            # Marks as modified to save later
            modified = True
        else:
            # Reading existing values
            for key, value in section.items():
                if not hasattr(section_cls, key):
                    logger.warning(f"Unknown config field: {section_name}.{key}")
                    continue
                setattr(section_cls, key, value)
            if len(section) < len(section_cls.to_dict()):
                # Some fields are missing
                for key, value in section_cls.to_dict().items():
                    if key not in section:
                        logger.warning(f"Missing config field: {section_name}.{key}, adding default.")
                        section.add(key, value)
                        modified = True

    if modified:
        with open(path, "w", encoding="utf-8") as f:
            f.write(tomlkit.dumps(data))

        logger.info(f"Updated config file at: {path}")

    logger.info(f"Loaded config file from: {path}")
