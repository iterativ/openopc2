import logging
import logging.config
import os
from pythonjsonlogger.jsonlogger import JsonFormatter
import structlog
import sys


# This code is based on the following example: https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging

def configure_logging(log_level: str, disable_colors: bool, no_console: bool) -> None:
    if no_console:
        sys.stdout = open(os.devnull, 'w')

    paths = ['logs/']
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    log_level = log_level.upper()

    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S", utc=False)
    pre_chain = [
        # Add the log level and a timestamp to the event_dict if the log entry
        # is not from structlog.
        structlog.stdlib.add_log_level,
        # Add extra attributes of LogRecord objects to the event dictionary
        # so that values passed in the extra parameter of log methods pass
        # through to log output.
        structlog.stdlib.ExtraAdder(),
        timestamper,
    ]

    def extract_from_record(_, __, event_dict):
        """
        Extract special keys from the LogRecord to add them in console
        """
        record = event_dict["_record"]
        event_dict["f"] = f"{record.filename}:{record.lineno}"
        return event_dict

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "plain": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(colors=False),
                ],
                "foreign_pre_chain": pre_chain,
            },
            "colored": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processors": [
                    extract_from_record,
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(colors=not disable_colors),
                ],
                "foreign_pre_chain": pre_chain,
            },
            'json': {
                '()': JsonFormatter,
                'format': '%(asctime)s %(msecs)03d %(process)d %(thread)d %(levelname)s %(name)s %(filename)s %(lineno)d %(funcName)s %(message)s',
                'datefmt': '%Y-%m-%dT%H:%M:%S',
            },
        },
        "handlers": {
            "default": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "colored",
            },
            'json-file': {
                "level": "DEBUG",
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logs/openopc2_log.json',
                'maxBytes': 10_000_000,
                'backupCount': 10,
                'formatter': 'json',
            },

        },
        "loggers": {
            "": {
                "handlers": ["json-file"] if no_console else ["default", "json-file"],
                "level": "DEBUG",
                "propagate": True,
            },
        }
    })
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


configure_logging("INFO", False, False)
