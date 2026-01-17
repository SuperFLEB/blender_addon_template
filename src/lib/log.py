import sys
import typing
from enum import IntEnum
from .ESQ import ESQ, ESQStyle, ESQBlock, join


class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class ConsoleLogger:
    style: ESQStyle | None
    default_level: LogLevel

    def __init__(self, name: str, style: ESQStyle | None = None, default_level: LogLevel = LogLevel.INFO,
                 stdout: typing.TextIO = sys.stdout, stderr: typing.TextIO = sys.stderr,
                 stdout_level: LogLevel = LogLevel.INFO, stderr_level: LogLevel = LogLevel.ERROR):
        self.name = name
        self.style = ESQ.default if style is None else style
        self.default_level = default_level

    def log(self, level: LogLevel = LogLevel.INFO, *messages) -> None:
        log_line = join(messages, " ")
        if level == LogLevel.DEBUG:
            print(ESQ.dim(self.style(self._badge(level) + log_line)))
        else:
            print(self.style(self._badge(level) + log_line))

    def _badge(self, level: LogLevel) -> str:
        level_tag = "" if level is LogLevel.INFO else f":{level.name}"
        match level:
            case LogLevel.DEBUG: level_tag = ESQ.green(":DEBUG")
            case LogLevel.INFO: level_tag = ESQ.cyan(":INFO")
            case LogLevel.WARNING: level_tag = ESQ.black.on.yellow(":WARNING")
            case LogLevel.ERROR: level_tag = ESQ.bright.yellow.on.red(":ERROR")
            case LogLevel.CRITICAL: level_tag = ESQ.red.on.bright.yellow(":CRITICAL")
            case _: level_tag = ""

        return f"[{self.name}{level_tag and ':'}{level_tag}] "

    def debug(self, *messages) -> None:
        self.log(LogLevel.DEBUG, *messages)

    def info(self, *messages) -> None:
        self.log(LogLevel.INFO, *messages)

    def warning(self, *messages) -> None:
        self.log(LogLevel.WARNING, *messages)

    def error(self, *messages) -> None:
        self.log(LogLevel.ERROR, *messages)

    def critical(self, *messages) -> None:
        self.log(LogLevel.CRITICAL, *messages)

