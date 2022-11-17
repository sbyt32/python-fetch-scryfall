import arrow
import logging
import logging.config
local = arrow.utcnow().format("YYYY-MM-DD")

LOGGER_NAME     =   "Price Tracker" # ? Filler name
BASIC_FORMAT    =   "%(asctime)s | %(levelname)-8s | %(filename)-20s | %(message)s"
CONSOLE_FORMAT  =   "%(asctime)s | %(levelname)-8s | %(filename)-20s | %(message)s"
FILE_FORMAT     =   "%(asctime)s | %(levelname)-8s | %(filename)-20s | %(message)s"
ERROR_FORMAT    =   "%(asctime)s | %(levelname)-8s | %(pathname)-20s | %(lineno)-8s | %(message)s"

# TODO:
# EXCEPT_FORMAT   =   "%(asctime)s | %(levelname)-8s | %(filename)-20s | %(message)s"


log_file_info   = f"logs/{local.format('MMM_DD_YY').lower()}.log"

def log_setup():
    log_config = {
        'name': LOGGER_NAME,
        "version": 1,
        'formatters': {
            'console_format': {
                'format': CONSOLE_FORMAT
            },
            'file_format': {
                'format': FILE_FORMAT
            },
            'file_format_error': {
                'format': ERROR_FORMAT
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': logging.INFO,
                'formatter': 'console_format',
            },
            'file_info': {
                'class': 'logging.FileHandler',
                'level': logging.INFO,
                'formatter': 'file_format',
                'filename': log_file_info,
            },
            'file_debug': {
                'class': 'logging.FileHandler',
                'level': logging.DEBUG,
                'formatter': 'file_format',
                'filename': log_file_info,
            },
            'file_error': {
                'class': 'logging.FileHandler',
                'level': logging.ERROR,
                'formatter': 'file_format_error',
                'filename': log_file_info,
            }
        },
        'root': {
            'level': logging.DEBUG,
            'propogate': True,
            'handlers': [
                'console',
                'file_info',
                'file_debug',
                'file_error'
            ]
        },
        'loggers': {
            LOGGER_NAME: {
                'level': logging.INFO,
                'propogate': True,
                'handlers': [
                    'console',
                    'file_info',
                    'file_debug',
                    'file_error'
                ],
            }
        }
    }

    logging.config.dictConfig(log_config)