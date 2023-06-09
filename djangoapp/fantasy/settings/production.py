from django.core.management.utils import get_random_secret_key
import dj_database_url
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = False
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
INTERNAL_IPS = ["127.0.0.1", "localhost"]

INSTALLED_APPS += []

MIDDLEWARE += []

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# only temp details.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db",
        "USER": "db",
        "PASSWORD": "AVNS_jeOxTgG6bTTyKq-3X8R",
        "HOST": "app-c0861794-c49f-449f-a5c1-8d2530eecb3e-do-user-11775277-0.b.db.ondigitalocean.com",
        "PORT": "25060",
        }
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

sentry_sdk.init(
    dsn="https://7d3c74e60809430dbfc65cd8365983e2@o283236.ingest.sentry.io/4505154295169024",
    integrations=[
        DjangoIntegration(),
    ],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
