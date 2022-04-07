import logging
import logging.config
from logging import Logger


class AppLogger(Logger):
    def __init__(self):
        self.LoggingConfig = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default_formatter': {
                    'format': '[%(levelname)s:%(asctime)s] %(funcName)s - %(message)s'
                },
            },
            'handlers': {
                'stream_handler': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default_formatter',
                },
                'rotating_file_handler': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'formatter': 'default_formatter',
                    'filename': 'whatshappend.log',
                    'mode': 'a',
                    'maxBytes': 1024,
                    'backupCount': 5
                },
            },
            'loggers': {
                'debug_log': {
                    'handlers': ['stream_handler', 'rotating_file_handler'],
                    'level': 'DEBUG',
                    'propagate': False
                },
                'info_log': {
                    'handlers': ['rotating_file_handler'],
                    'level': 'INFO',
                    'propagate': False
                },
                'error_log': {
                    'handlers': ['rotating_file_handler'],
                    'level': 'ERROR',
                    'propagate': False
                },
                'warning_log': {
                    'handlers': ['rotating_file_handler'],
                    'level': 'WARNING',
                    'propagate': False
                },
                'critical_log': {
                    'handlers': ['rotating_file_handler'],
                    'level': 'CRITICAL',
                    'propagate': False
                }
            }
        }
        logging.config.dictConfig(self.LoggingConfig)

    def debug_log(self, log_message):
        logger = logging.getLogger('debug_log')
        return logger.debug(log_message)

    def info_log(self, log_message):
        logger = logging.getLogger('info_log')
        return logger.info(log_message)

    def error_log(self, log_message):
        logger = logging.getLogger('error_log')
        return logger.error(log_message)

    def warning_log(self, log_message):
        logger = logging.getLogger('warning_log')
        return logger.warning(log_message)
    
    def critical_log(self, log_message):
        logger = logging.getLogger('critical_log')
        return logger.critical(log_message)