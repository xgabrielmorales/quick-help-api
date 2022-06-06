import os
from quick_project.settings.base import *

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS += [
    # Other apps for production site
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ["PRODUCTION_DB_NAME"],
        "USER": os.environ["PRODUCTION_DB_USER"],
        "PASSWORD": os.environ["PRODUCTION_DB_PASSWORD"],
        "HOST": os.environ["PRODUCTION_DB_HOST"],
        "PORT": os.environ["PRODUCTION_DB_PORT"],
    }
}
