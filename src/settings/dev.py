from .base import *

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SECRET_KEY = "django-insecure-kmjazim6m&0r^%!!(s99&z(d0jumq6!fs8$$qoyg&p_-vwsx!&"

ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


try:
    from .local import *
except ImportError:
    pass
