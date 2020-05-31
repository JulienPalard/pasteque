import os
import django

### Useful constants

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

### Customize/configure Pasteque

DISPLAY_NAME = "Pasteque"
COMPRESS_ENABLED = False
SECRET_KEY = "change_me"
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
TIME_ZONE = "Europe/Brussels"
LANGUAGE_CODE = "fr-FR"
DICT = os.path.join(SITE_ROOT, "dict", "french")
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (("user", "user@hostname.domain"),)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": os.path.join(SITE_ROOT, "var", "db", "webtools.sqlite3"),
        # The following settings are not used with sqlite3:
        "USER": "",
        "PASSWORD": "",
        "HOST": "",  # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        "PORT": "",  # Set to empty string for default.
    }
}

### End of customisation

APP_NAME = "Pasteque"
APP_VERSION = "v0.1"
SITE_ID = 1
MANAGERS = ADMINS
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_URL = ""
CACHE_PATH = os.path.join(SITE_ROOT, "var", "pygments-static")
COMPRESS_ROOT = os.path.join(SITE_ROOT, "static")
MEDIA_ROOT = os.path.join(SITE_ROOT, "assets")
STATIC_ROOT = os.path.join(SITE_ROOT, "static")
STATIC_URL = "/static/"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)
TEMPLATE_LOADERS = (
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "paste.context_processors.app_details",
            ],
        },
    },
]

MIDDLEWARE = [
    "paste.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
]

ROOT_URLCONF = "webtools.urls"
WSGI_APPLICATION = "webtools.wsgi.application"
INSTALLED_APPS = (
    "django.contrib.staticfiles",
    "django.contrib.contenttypes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.messages",
    "django.contrib.sessions",
    "compressor",
    "paste",
)

PASTE = {
    "has_title": False,
    "has_expire_by_views": False,
    "has_meta_table": False,
    "show_char_left": False,
    "private_by_default": True,
    "enabled_renderers": ["pygments", "raw"],
    "default_renderer": "pygments",
    "max_characters": 100000,
    "default_lifetime": 60 * 24 * 7 * 365,
    "default_language": "Python",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {"level": "DEBUG", "class": "logging.StreamHandler",},
        "logfile": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(SITE_ROOT, "var", "logs", "error.log"),
            "maxBytes": 50000,
            "backupCount": 2,
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console", "logfile"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
