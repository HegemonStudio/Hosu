from typing import Dict

from core.logger import get_logger
from core.variables import Variable

logger = get_logger(__name__)


class VariableMap:
    def __init__(self):
        self._vars: Dict[str, Variable] = {}

    def set(self, name: str, var: Variable):
        name = name.upper()
        self._vars[name] = var

    def get_variable(self, name: str) -> Variable | None:
        name = name.upper()
        if name not in self._vars:
            return None
        return self._vars[name]

    def __getitem__(self, name: str) -> Variable | None:
        return self.get_variable(name)

    def __len__(self):
        return len(self._vars)

    def has(self, name: str) -> bool:
        name = name.upper()
        return name in self._vars

    def get_text(self, name: str) -> str:
        name = name.upper()
        if name not in self._vars:
            logger.warning(f"Variable '{name}' not found in VariableMap")
            return f"{{{name}}}"
        return self._vars[name].get_text()

    def __repr__(self):
        return f"VariableMap({self._vars})"
