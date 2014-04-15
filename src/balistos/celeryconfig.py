# -*- coding: utf-8 -*-
"""Config for celery workers"""

from datetime import timedelta

## Broker settings.
BROKER_URL = 'redis://localhost:6379/0'

# List of modules to import when celery starts.
CELERY_IMPORTS = ('balistos.tasks', )

#CELERY_ALWAYS_EAGER = True

CELERYBEAT_SCHEDULE = {
    'check_playlists': {
        'task': 'balistos.tasks.check_playlists',
        'schedule': timedelta(seconds=3),
    },
}
