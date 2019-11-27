# import os
# from celery import Celery
# from django.conf import settings
#
# app = Celery('django_rest_framework')
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_framework.settings')
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)




# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_rest_framework.settings')
os.environ.setdefault('DJANGO_IN_CELERY', 'true')

app = Celery('django_rest_framework')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()