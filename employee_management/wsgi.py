"""
WSGI config for employee_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#from whitenoise.django import DjangoWhiteNoise

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.settings')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_management.prod_settings')

application = get_wsgi_application()
#application = DjangoWhiteNoise(application)