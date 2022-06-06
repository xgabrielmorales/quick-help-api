from quick_project.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "quick-database",
        "USER": "quick-user",
        "PASSWORD": "quick-user-password",
        "HOST": "localhost",
        "PORT": 5432,
    }
}
