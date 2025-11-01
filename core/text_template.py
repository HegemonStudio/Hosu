from dataclasses import dataclass
from typing import List, Union, Optional, Callable, Any

from core.logger import get_logger
from core.variable_map import VariableMap

logger = get_logger(__name__)


@dataclass
class Literal:
    text: str


@dataclass
class Variable:
    name: str


Token = Union[Literal, Variable]


class TemplateLexer:
    def __init__(self, content: str):
        # We use list of chars to use slices.
        self.content: List[str] = list(content)

    def empty(self) -> bool:
        return len(self.content) == 0

    def peek(self) -> Optional[str]:
        return self.content[0] if not self.empty() else None

    def chop(self, n: int) -> str:
        """
        Chops first n chars from the buffer and returns them as string
        """
        token = self.content[:n]
        self.content = self.content[n:]
        return ''.join(token)

    def chop_while(self, predicate: Callable[[str], bool]) -> str:
        """
        Chops characters while predicate return true.
        Returns them as string.
        """
        n = 0
        while n < len(self.content) and predicate(self.content[n]):
            n += 1
        return self.chop(n)

    def chop_until(self, predicate: Callable[[str], bool]) -> str:
        """
        Chops characters until predicate return true.
        Returns them as string.
        """
        n = 0
        while n < len(self.content) and not predicate(self.content[n]):
            n += 1
        return self.chop(n)

    def trim(self) -> None:
        n = 0
        while n < len(self.content) and self.content[n].isspace():
            n += 1
        self.content = self.content[n:]

    def next_token(self) -> Optional[Token]:
        """
        Extracts the next token
        """
        if self.empty():
            return None
        # If next char is '{' start reading variable
        if self.peek() == '{':
            self.chop(1)  # skip {
            self.trim()
            varname = self.chop_until(lambda x: x == '}').rstrip().upper().replace(' ', '_')
            if self.empty():
                logger.warning(f"Unclosed variable: {varname}")
                return Variable(varname)
            self.chop(1)  # skip }
            return Variable(varname)
        else:
            # Literal until '{'
            text = self.chop_until(lambda c: c == '{')
            return Literal(text)

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while not self.empty():
            token = self.next_token()
            if token:
                tokens.append(token)
        return tokens


class TextTemplate:
    """
    Supports plain text and {VAR} placeholders.
    """

    def __init__(self, text: str):
        self.original = text
        self.tokens: List[Token] = TemplateLexer(text).tokenize()

    def resolve(self, variables: Union[dict[str, Any], VariableMap]) -> str:
        if isinstance(variables, VariableMap):
            return self.resolve_varmap(variables)
        elif isinstance(variables, dict):
            return self.resolve_dict(variables)
        else:
            raise TypeError(f"Unsupported variable container: {type(variables)}")

    def resolve_dict(self, variables: dict[str, Any]) -> str:
        parts: List[str] = []
        for token in self.tokens:
            if isinstance(token, Literal):
                parts.append(token.text)
            elif isinstance(token, Variable):
                val = variables.get(token.name)
                if val is None:
                    logger.warning(f"Missing variable {{{token.name}}}")
                    parts.append(f"{{{token.name}}}")
                else:
                    parts.append(str(val))
            else:
                logger.warning(f"Unsupported token type: {type(token)}")
        return "".join(parts)

    def resolve_varmap(self, variables: VariableMap) -> str:
        parts: List[str] = []
        for token in self.tokens:
            if isinstance(token, Literal):
                parts.append(token.text)
            elif isinstance(token, Variable):
                if not variables.has(token.name):
                    logger.warning(f"Missing variable {{{token.name}}}")
                text = variables.get_text(token.name)
                parts.append(text)
            else:
                logger.warning(f"Unsupported token type: {type(token)}")
        return "".join(parts)

    def get_texts(self) -> List[str]:
        parts: List[str] = []
        for token in self.tokens:
            if isinstance(token, Literal):
                parts.append(token.text)
        return parts

    def get_vars(self) -> List[str]:
        parts: List[str] = []
        for token in self.tokens:
            if isinstance(token, Variable):
                parts.append(token.name)
        return parts

    def get_tokens(self) -> List[Token]:
        return self.tokens

    def __str__(self):
        """
        String representation of the template (unresolved).
        """
        parts: List[str] = []
        for token in self.tokens:
            if isinstance(token, Literal):
                parts.append(token.text)
            else:
                parts.append(f"{{{token.name}}}")
        return "".join(parts)

    def __repr__(self):
        return f"{self.__class__.__name__}{self.__str__()}"
