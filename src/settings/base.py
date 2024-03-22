import os
import dj_database_url

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "c6u0-9c!7nilj_ysatsda0(f@e_2mws2f!6m0n^o*4#*q#kzp)"
DEBUG = True
DEVELOPMENT_MODE = True

INTERNAL_IPS = [
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    'django_countries',
    'strategies',
    'investment',
    'advisors',
    'team',
    'base',
    "home",
    "crispy_forms",
    "crispy_bootstrap5",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.api.v2",
    "wagtail.locales",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.table_block",
    "wagtail.contrib.typed_table_block",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.settings",
    "wagtail.contrib.simple_translation",
    "wagtail.contrib.styleguide",
    "wagtail",
    "rest_framework",
    "modelcluster",
    "taggit",
    "wagtailfontawesomesvg",
    "debug_toolbar",
    "django_extensions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
ROOT_URLCONF = "src.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if "DATABASE_URL" in os.environ:
    DATABASES = {"default": dj_database_url.config(conn_max_age=500)}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "scipiosqlitedb"),
        },
        "mysqldb": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.environ.get("MYSQL_DATABASE", ""),
            "USER": os.environ.get("MYSQL_USER", ""),
            "PASSWORD": os.environ.get("MYSQL_PASSWORD", ""),
            "HOST": os.environ.get("MYSQL_HOST", ""),
            "PORT": os.environ.get("MYSQL_PORT", ""),
        },
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# JavaScript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Wagtail settings

WAGTAIL_SITE_NAME = "scipio"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
        "INDEX": "scipio",

    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"

WAGTAIL_I18N_ENABLED = True

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES = [
    ("en", "English"),
    ("de", "Deutsch"),
    ("ar", "العربيّة"),
]


if "CSP_DEFAULT_SRC" in os.environ:
    MIDDLEWARE.append("csp.middleware.CSPMiddleware")

    CSP_REPORT_ONLY = True


    CSP_DEFAULT_SRC = os.environ.get("CSP_DEFAULT_SRC").split(",")
    if "CSP_SCRIPT_SRC" in os.environ:
        CSP_SCRIPT_SRC = os.environ.get("CSP_SCRIPT_SRC").split(",")
    if "CSP_STYLE_SRC" in os.environ:
        CSP_STYLE_SRC = os.environ.get("CSP_STYLE_SRC").split(",")
    if "CSP_IMG_SRC" in os.environ:
        CSP_IMG_SRC = os.environ.get("CSP_IMG_SRC").split(",")
    if "CSP_CONNECT_SRC" in os.environ:
        CSP_CONNECT_SRC = os.environ.get("CSP_CONNECT_SRC").split(",")
    if "CSP_FONT_SRC" in os.environ:
        CSP_FONT_SRC = os.environ.get("CSP_FONT_SRC").split(",")
    if "CSP_BASE_URI" in os.environ:
        CSP_BASE_URI = os.environ.get("CSP_BASE_URI").split(",")
    if "CSP_OBJECT_SRC" in os.environ:
        CSP_OBJECT_SRC = os.environ.get("CSP_OBJECT_SRC").split(",")

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
