from enum import Enum


class ProtocolMode(str, Enum):
    """
    Protocol mode
    """
    COM = "com"
    GATEWAY = "gateway"


class DataSource(str, Enum):
    """
    Data source for read
    """
    CACHE = "cache"
    DEVICE = "device"
    HYBRID = "hybrid"


class LogLevel(str, Enum):
    """
    Log level
    """
    CRITICAL = "CRITICAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
