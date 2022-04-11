import logging
from logging import config, getLogger


dictLogging = {
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
            'maxBytes': 2*1024*1024,
            'backupCount': 2
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
            'handlers': ['stream_handler', 'rotating_file_handler'],
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

def AppLoger(logger_name):
    config.dictConfig(dictLogging)

    Loger = getLogger(logger_name)

    return Loger
  

    

        

    