import os
from celery import celery
from django.confg import settings


# for the Celery command-line program
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zxk.settings")

# we create an instance of our application
app = Celery('zxk')

# We load any custom configuration from our project settings
app.config_from_object('django.conf:settings')

# we tell Celery to auto-discover asynchronous tasks for the applications 
# listed in the INSTALLED_APPS setting. Celery will look for a tasks.py file 
# in each application directory to load asynchronous tasks defined in it.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)