from __future__ import annotations

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DEBUG = False
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = "THISisNOTsecretADFKWERdklafda8324jbnkafd"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mem_db",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    "django_nh3",
    "tests",
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

NH3_ALLOWED_ATTRIBUTES = {
    "a": {"style"},
    "img": {"src"},
}
NH3_FILTER_STYLE_PROPERTIES = {"text-align"}
NH3_ALLOWED_TAGS = {"a"}
