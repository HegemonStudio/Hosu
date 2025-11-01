from dataclasses import dataclass
from typing import List, Dict, Union

from core.logger import get_logger

logger = get_logger(__name__)

"""
Tokens
"""
@dataclass
class Literal:
    text: str

@dataclass
class Variable:
    name: str

Token = Union[Literal, Variable]

class TextTemplate:
    """
    Supports plain text and {VAR} placeholders.
    """
    def __init__(self, text: str):
        self.original = text
        self.tokens: List[Token] = self._tokenize(text)

    def _tokenize(self, text: str) -> List[Token]:
        tokens: List[Token] = []
        buffer = ""
        inside_var = False
        buffer_var = ""

        for ch in text:
            if ch == '{' and not inside_var:
                # flush current literal
                if buffer:
                    tokens.append(Literal(buffer))
                    buffer = ""
                # start reading var
                inside_var = True
                var_buffer = ""
            elif ch == '}' and inside_var:
                # flush current var
                inside_var = False
                tokens.append(Variable(buffer_var))
                buffer_var = ""
            elif inside:
                buffer_var += ch
            else:
                buffer += ch
        
        if buffer:
            tokens.append(Literal(buffer))

        return tokens
