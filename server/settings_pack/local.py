import os

from .base import *

DEBUG = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings.local")
