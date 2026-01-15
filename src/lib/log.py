import sys
import typing
from enum import IntEnum
from .ESQ import ESQ, ESQStyle


class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class ConsoleLogger:
    style: ESQStyle | None
    default_level: LogLevel
    stdout_level: LogLevel
    stderr_level: LogLevel
    stdout: typing.TextIO | None
    stderr: typing.TextIO | None

    def __init__(self, name: str, style: ESQStyle | None, default_level: LogLevel = LogLevel.INFO,
                 stdout: typing.TextIO = sys.stdout, stderr: typing.TextIO = sys.stderr,
                 stdout_level: LogLevel = LogLevel.INFO, stderr_level: LogLevel = LogLevel.ERROR):
        self.name = name
        self.style = ESQ.default if style is None else style
        self.default_level = default_level

    def log(self, level: LogLevel = LogLevel.INFO, *messages) -> None:
        if level < self.stdout_level and level < self.stderr_level: return
        destination = self.stdout if level <= self.stderr_level else self.stderr
        level_tag = "" if level is LogLevel.INFO else f":{LogLevel.name}"
        log_line = "".join([str(m) for m in messages])
        print(self.style(f"[{self.name}{level_tag}] {log_line}"), file=destination)

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
