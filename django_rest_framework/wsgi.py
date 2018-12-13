"""
WSGI config for django_rest_framework project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('DEV') is True:
   os.environ.setdefault("DJANGO_SETTINGS_MODULE","django_rest_framework.settings.dev")
else:
   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_rest_framework.settings")

application = get_wsgi_application()
