import typing
import os
from enum import Enum
from typing import Any, Generator

_ESC = "\033"
# Lists of escape codes for each color/style
_escape_sequences = (
    ("39", "30", "31", "32", "33", "34", "35", "36", "37", "90", "91", "92", "93", "94", "95", "96", "97"),
    ("49", "40", "41", "42", "43", "44", "45", "46", "47", "100", "101", "102", "103", "104", "105", "106", "107"),
    ("22;23;24;25;27", "1", "2", "3", "4", "5", "6", "7", "8", "9"),
    ("22;23;24;25;27", "22", "22", "23", "24", "25", "25", "27", "28", "29")
)

class _ColorEnum(int, Enum):
    # Colors
    default = 0
    black = 1
    red = 2
    green = 3
    brown = 4
    dark_yellow = 4
    yellow = 4
    blue = 5
    magenta = 6
    cyan = 7
    white = 8
    light_gray = 8
    gray = 9
    bright_black = 9
    bright_red = 10
    bright_green = 11
    bright_yellow = 12
    bright_blue = 13
    bright_magenta = 14
    bright_cyan = 15
    bright_white = 16


class _FXEnum(int, Enum):
    # Effects
    normal = 0
    bold = 0b0_0000_0001
    dim = 0b0_0000_0010
    italic = 0b0_0000_0100
    underline = 0b0_0000_1000
    blink = 0b0_0001_0000
    blink2 = 0b0_0010_0000
    reverse = 0b0_0100_0000
    hidden = 0b0_1000_0000
    strike = 0b1_0000_0000


def _directive(from_state: "_ESQState", to_state: "_ESQState") -> "_ESQDirective":
    if to_state.fg == from_state.fg:
        fg = None
    else:
        fg = to_state.fg

    if to_state.bg == from_state.bg:
        bg = None
    else:
        bg = to_state.bg

    fxon = to_state.fx & (from_state.fx ^ 0b1_1111_1111)
    fxoff = from_state.fx & (to_state.fx ^ 0b1_1111_1111)

    return _ESQDirective(fg, bg, fxon, fxoff)


def _apply(from_state: "_ESQState | None", directive: "_ESQDirective | None" = None) -> "_ESQState":
    if from_state is None:
        from_state = _ESQState(_ColorEnum.default, _ColorEnum.default, 0)

    if directive is None:
        directive = _ESQDirective()

    fg = from_state.fg if directive.fg is None else directive.fg
    bg = from_state.bg if directive.bg is None else directive.bg

    fx = from_state.fx | (directive.fxon or 0)
    fx = fx & ((directive.fxoff or 0) ^ 0b1_1111_1111)

    return _ESQState(fg, bg, fx)


class _ESQDirective:
    fg: _ColorEnum | None
    bg: _ColorEnum | None
    fxon: int | None
    fxoff: int | None

    def __init__(self, fg: _ColorEnum | None = None, bg: _ColorEnum | None = None, fxon: _FXEnum | int | None = None,
                 fxoff: _FXEnum | int | None = None):
        self.fg = fg
        self.bg = bg
        self.fxon = fxon.value if isinstance(fxon, _FXEnum) else fxon
        self.fxoff = fxoff.value if isinstance(fxoff, _FXEnum) else fxoff

    def esc(self) -> str:
        codes = []
        if self.fg is not None:
            codes.append(_escape_sequences[0][self.fg.value])
        if self.bg is not None:
            codes.append(_escape_sequences[1][self.bg.value])
        for bit in range(9):
            if self.fxon is not None and self.fxon & (1 << bit):
                codes.append(_escape_sequences[2][bit + 1])
            if self.fxoff is not None and self.fxoff & (1 << bit):
                codes.append(_escape_sequences[3][bit + 1])

        if len(codes) == 0: return ""

        return "".join([_ESC + "[", ";".join(codes), "m"])


class _ESQState:
    fg: _ColorEnum
    bg: _ColorEnum
    fx: int = 0

    def __init__(self, fg: _ColorEnum = _ColorEnum.default, bg: _ColorEnum = _ColorEnum.default, fx: int = 0):
        self.fg = fg
        self.bg = bg
        self.fx = fx

    def apply(self, directive: _ESQDirective | None) -> "_ESQState":
        return _apply(self, directive) if directive is not None else self

    def revert_directive(self, previous: "_ESQState") -> "_ESQDirective":
        return _directive(self, previous)


class _Concatenation:
    parts: list

    def __init__(self, *parts: typing.Any):
        self.parts = list(parts)

    def append(self, *parts: typing.Any):
        self.parts.extend(parts)

    def extend(self, more: typing.Iterable):
        self.parts.extend(more)

    def __add__(self, right):
        self.parts.append(right)
        return self

    def __radd__(self, left):
        if isinstance(left, _Concatenation):
            left.parts.extend(self.parts)
            return left
        return _Concatenation(left, *self.parts)

    def __len__(self) -> int:
        return len(self.parts)

    def __iter__(self) -> Generator:
        yield from self.parts

    def __str__(self) -> str:
        return "".join((p.render(_ESQState()) if isinstance(p, _ESQBlock) else str(p) for p in self.parts))


class _ESQBlock:
    directive: _ESQDirective | None = None
    children: list

    def __init__(self, directive: _ESQDirective | None = None, *children: typing.Any):
        self.directive = directive or _ESQDirective()
        self.children = list(children)

    def __str__(self) -> str:
        return self.render(_ESQState())

    def _render_part(self, part: "_ESQBlock | str", state: _ESQState) -> str:
        if isinstance(part, _ESQBlock):
            return part.render(state)
        if isinstance(part, _Concatenation):
            return "".join((self._render_part(item, state) for item in part))
        return str(part)

    def render(self, parent_state: _ESQState | None) -> str:
        result = []
        if self.directive is not None:
            result.append(self.directive.esc())
        self_state = (parent_state or _ESQState(_ColorEnum.default, _ColorEnum.default, 0)).apply(self.directive)
        result.extend([self._render_part(child, self_state) for child in self.children])
        result.append(self_state.revert_directive(parent_state).esc())
        return "".join(result)

    def __add__(self, right) -> "_Concatenation":
        parts = right.parts if isinstance(right, _Concatenation) else right
        return _Concatenation(self, parts)

    def __radd__(self, left) -> "_Concatenation":
        if isinstance(left, _Concatenation):
            left.append(self)
            return left
        return _Concatenation(left, self)


class _ESQDirectiveChain:
    """
    A chain of directives applied to one final function call.
    """
    directive: _ESQDirective
    kw_on: bool = False
    kw_not: bool = False

    def __init__(self) -> None:
        self.directive = _ESQDirective(None, None, None, None)

    def __call__(self, *children: typing.Any) -> _ESQBlock:
        return _ESQBlock(self.directive, *children)

    def __getattr__(self, name: str) -> "_ESQDirectiveChain":
        if name == "on":
            self.kw_on = True
            return self
        if name == "not":
            self.kw_not = True
            return self

        if self.kw_on:
            self.kw_on = False
            if name in _ColorEnum.__members__:
                name = f"on_{name}"

        if self.kw_not:
            self.kw_not = False
            if name in _FXEnum.__members__:
                name = f"not_{name}"

        if name.startswith("on_") and name[3:] in _ColorEnum.__members__:
            self.directive.bg = getattr(_ColorEnum, name[3:])
        elif name.startswith("not_") and name[4:] in _FXEnum.__members__:
            self.directive.fxoff = getattr(_FXEnum, name[4:])
        elif name in _FXEnum.__members__:
            self.directive.fxon = getattr(_FXEnum, name)
        elif name in _ColorEnum.__members__:
            self.directive.fg = getattr(_ColorEnum, name)
        return self


def debug_ansi() -> None:
    global _ESC, _escape_sequences
    _ESC = "{ESC}"
    _escape_sequences = (
        tuple(f"<fg={_ColorEnum(idx).name}>" for idx in range(len(_escape_sequences[0]))),
        tuple(f"<bg={_ColorEnum(idx).name}>" for idx in range(len(_escape_sequences[0]))),
        tuple(f"<+{m.name}>" for m in _FXEnum),
        tuple(f"<-{m.name}>" for m in _FXEnum),
    )


if os.environ.get("DEBUG_ANSI", "0") == "1":
    debug_ansi()


class _ESQ:
    def __getattr__(self, name: str) -> _ESQDirectiveChain:
        return _ESQDirectiveChain().__getattr__(name)


ESQ = _ESQ()

