from enum import IntEnum

class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

class ConsoleLogger:
    def __init__(self, name: str, default_level: LogLevel = LogLevel.INFO):


    def log(self, level: LogLevel, message: str) -> None:

        print(f"[{level.name}] {message}")