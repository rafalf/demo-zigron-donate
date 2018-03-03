import os
import yaml

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
BASE_URL = "http://th.zigron.com"
CAMPAIGN_URL = "http://th.zigron.com/donate/campaign/{}/"

LOGGING_CONFIG = {
    'formatters': {
        'brief': {
            'format': '[%(asctime)s][%(levelname)s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        }
    },
    'loggers': {
        'main': {
            'propagate': False,
            'handlers': ['console'],
            'level': 'INFO'
        }
    },
    'version': 1
}
