import logging.config

log_conf = {
    "version": 1,
    "formatters": {
        "simple_form": {
            "format": "%(asctime)s - [%(levelname)s]\t- %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %("
                      "message)s",
        },
        "form_with_stdout": {
            "format": "%(asctime)s - [%(levelname)s]\t- %(funcName)s\t- %(message)s",
        },
    },
    "handlers": {
        "stream_handler": {
            "level": "INFO",
            "formatter": "form_with_stdout",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file_handler": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "cache.log",
            "formatter": "simple_form",
        },

    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["file_handler"],
        },
        "main_with_stdout": {
            "level": "DEBUG",
            "handlers": ["file_handler", "stream_handler"],
            "propagate": False,
        },
    },
}
logging.config.dictConfig(log_conf)
