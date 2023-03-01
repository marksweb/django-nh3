from __future__ import annotations

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = "THISisNOTsecretADFKWERdklafda8324jbnkafd"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    "tests.testapp",
    "django_nh3",
]

ROOT_URLCONF = "tests.urls"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": ["django.contrib.auth.context_processors.auth"]
        },
    }
]
