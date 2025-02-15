import os
import warnings
from email.utils import parseaddr

from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as messages

import environ


env = environ.Env(
    DEBUG=(bool, False),
)  # set default values and casting

# silence warning from .env not existing
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    environ.Env.read_env()  # reading .env file


def mkpath(*parts):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", *parts))


MKPATH = mkpath

DEBUG = env.bool("DEBUG", default=False)

CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_URLS_REGEX = r"^/(api|oauth2)/.*$"
CORS_ORIGIN_WHITELIST = env("CORS_ORIGIN_WHITELIST", default="").split()

ADMINS = [parseaddr(addr) for addr in env("ADMINS", default="").split(",") if addr]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "HOST": env("POSTGRES_HOSTNAME", default="postgres"),
        "NAME": env("POSTGRES_DATABASE", default="kompassi"),
        "USER": env("POSTGRES_USERNAME", default="kompassi"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="secret"),
        "OPTIONS": {
            "sslmode": env("POSTGRES_SSLMODE", default="allow"),
        },
        "ENGINE": "psqlextra.backend",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

CACHES = {
    "default": env.cache(default="locmemcache://"),
}

ALLOWED_HOSTS = env("ALLOWED_HOSTS", default="localhost").split()

TIME_ZONE = "Europe/Helsinki"

DATE_FORMAT = "j.n.Y"
SHORT_DATE_FORMAT = DATE_FORMAT
DATE_FORMAT_STRFTIME = "%d.%m.%Y"

DATETIME_FORMAT = "j.n.Y G:i:s"
SHORT_DATETIME_FORMAT = DATETIME_FORMAT
DATETIME_FORMAT_STRFTIME = "%d.%m.%Y %H:%M:%S"

LANGUAGE_CODE = "fi"
LANGUAGES = (
    ("fi", _("Finnish")),
    ("en", _("English")),
)
SITE_ID = 1
USE_I18N = True
USE_TZ = True

MEDIA_ROOT = mkpath("media")
MEDIA_URL = "/media/"
STATIC_ROOT = mkpath("static")
STATIC_URL = "/static/"

STATICFILES_DIRS = ()
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

SECRET_KEY = env.str("SECRET_KEY", default=("" if not DEBUG else "xxx"))

MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
    "csp.middleware.CSPMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "listings.middleware.ListingsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "core.middleware.PageWizardMiddleware",
    "core.middleware.EventOrganizationMiddleware",
    "django.middleware.locale.LocaleMiddleware",
)

ROOT_URLCONF = "kompassi.urls"
WSGI_APPLICATION = "kompassi.wsgi.application"
APPEND_SLASH = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            mkpath("kompassi", "templates"),
        ],
        "OPTIONS": {
            "context_processors": [
                "core.context_processors.core_context",
                "feedback.context_processors.feedback_context",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                # PyPugJS part:   ##############################
                (
                    "pypugjs.ext.django.Loader",
                    (
                        "django.template.loaders.filesystem.Loader",
                        "django.template.loaders.app_directories.Loader",
                    ),
                )
            ],
            "builtins": [
                "pypugjs.ext.django.templatetags",
            ],
        },
    },
]

TEST_RUNNER = "django.test.runner.DiscoverRunner"

INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "django.contrib.postgres",
    "psqlextra",
    "localized_fields",
    "pypugjs.ext.django",
    "crispy_forms",
    "oauth2_provider",
    "rest_framework",
    "bootstrap3",
    "lippukala",
    "paikkala",
    "core",
    "programme",
    "labour",
    "labour_common_qualifications",
    "tickets",
    "payments",
    "mailings",
    "api",
    "api_v2",
    "api_v3",
    "badges",
    "access",
    "membership",
    "intra",
    "desuprofile_integration",
    "enrollment",
    "feedback",
    "event_log",
    "surveys",
    "directory",
    "listings",
    "forms",
    "metrics",
    "background_tasks",
    "organizations.tracon_ry",
    "events.hitpoint2015",
    "events.kuplii2015",
    "events.mimicon2015",
    "events.yukicon2016",
    "events.finncon2016",
    "events.frostbite2016",
    "events.kuplii2016",
    "events.kawacon2016",
    "events.mimicon2016",
    "events.desucon2016",
    "events.lakeuscon2016",
    "events.hitpoint2017",
    "events.shippocon2016",
    "events.yukicon2017",
    "events.frostbite2017",
    "events.kuplii2017",
    "events.tracon2017",
    "events.popcult2017",
    "events.desucon2017",
    "events.ropecon2017",
    "events.kawacon2017",
    "events.worldcon75",
    "events.frostbite2018",
    "events.yukicon2018",
    "events.nippori2017",
    "events.kuplii2018",
    "events.tracon2018",
    "events.popcultday2018",
    "events.desucon2018",
    "events.matsucon2018",
    "events.ropecon2018",
    "events.finncon2018",
    "events.mimicon2018",
    "events.yukicon2019",
    "events.frostbite2019",
    "events.desucon2019",
    "events.tracon2019",
    "events.finncon2020",
    "events.kuplii2019",
    "events.nekocon2019",
    "events.popcult2019",
    "events.hitpoint2019",
    "events.hypecon2019",
    "events.ropecon2019",
    "events.matsucon2019",
    "events.finncon2019",
    "events.popcultnights2019",
    "events.frostbite2020",
    "events.desucon2020",
    "events.kuplii2020",
    "events.tracon2020",
    "events.nekocon2020",
    "events.ropecon2020",
    "events.tracrossf2019",
    "events.hypecon2020",
    "events.popcult2020",
    "events.concon17",
    "events.matsucon2020",
    "events.hitpoint2020",
    "events.ropecon2020vd",
    "events.ropecon2021",
    "events.tracon2021",
    "events.kuplii2021",
    "events.ropeconjvp2021",
    "events.desucon2022",
    "events.ropecon2022",
    "events.tracon2022",
    "events.kuplii2022",
    "events.finncon2022",
    "events.nekocon2022",
    "events.traconjvp2022",
    "events.traconjvk2022",
    "events.frostbite2023",
    "events.desucon2023",
    "events.matsucon2022",
    "events.concon18",
    "events.tracon2023",
    "events.ropecon2023",
    "events.kuplii2023",
    "events.hitpoint2023",
    "events.nekocon2023",
    "events.finncon2023",
    "events.tracon2023paidat",
    "events.cosvision2023",
    "events.shumicon2023",
    "events.matsucon2023",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console", "mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
        "celery": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "WARNING",
            "propagate": True,
        },
        "kompassi": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": True,
        },
        "requests": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "WARNING",
            "propagate": True,
        },
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"],
    "DEFAULT_RENDERER_CLASSES": (
        "api_v3.renderers.CamelCaseJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "api_v3.parsers.CamelCaseJSONRenderer",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
}

LOGIN_URL = "/login"

CRISPY_TEMPLATE_PACK = "bootstrap3"

AWS_STORAGE_BUCKET_NAME = env("MINIO_BUCKET_NAME", default="kompassi")
AWS_ACCESS_KEY_ID = env("MINIO_ACCESS_KEY_ID", default="kompassi")
AWS_SECRET_ACCESS_KEY = env("MINIO_SECRET_ACCESS_KEY", default="kompassi")
AWS_S3_ENDPOINT_URL = env("MINIO_ENDPOINT_URL", default="http://minio:9000")

# TODO script-src unsafe-inline needed at least by feedback.js. unsafe-eval needed by Knockout (roster.js).
# XXX style-src unsafe-inline is just basic plebbery and should be eradicated.
CSP_DEFAULT_SRC = "'none'"
CSP_SCRIPT_SRC = "'self' 'unsafe-inline' 'unsafe-eval'"
CSP_CONNECT_SRC = "'self'"
CSP_IMG_SRC = f"'self' {AWS_S3_ENDPOINT_URL}"
CSP_STYLE_SRC = "'self' 'unsafe-inline'"
CSP_FONT_SRC = "'self'"
CSP_FORM_ACTION = "'self'"
CSP_FRAME_ANCESTORS = "'none'"
X_FRAME_OPTIONS = "DENY"


MESSAGE_TAGS = {
    messages.ERROR: "danger",
}


KOMPASSI_APPLICATION_NAME = "Kompassi"
KOMPASSI_INSTALLATION_NAME = env("KOMPASSI_INSTALLATION_NAME", default="Kompassi (DEV)")
KOMPASSI_INSTALLATION_NAME_ILLATIVE = "Kompassin kehitys\u00ADinstanssiin" if DEBUG else "Kompassiin"
KOMPASSI_INSTALLATION_NAME_GENITIVE = "Kompassin kehitys\u00ADinstanssin" if DEBUG else "Kompassin"
KOMPASSI_INSTALLATION_NAME_PARTITIVE = "Kompassin kehitys\u00ADinstanssia" if DEBUG else "Kompassia"
KOMPASSI_INSTALLATION_SLUG = env("KOMPASSI_INSTALLATION_SLUG", default="turskadev")
KOMPASSI_PRIVACY_POLICY_URL = "https://ry.tracon.fi/tietosuoja/rekisteriselosteet/kompassi"
FEEDBACK_PRIVACY_POLICY_URL = "https://ry.tracon.fi/tietosuoja/rekisteriselosteet/kompassi-palaute"

# Confluence & co. require a group of users
KOMPASSI_NEW_USER_GROUPS = ["users"]
KOMPASSI_MAY_SEND_INFO_GROUP_NAME = "kompassi-maysendinfo"

AUTHENTICATION_BACKENDS = (
    "core.backends.PasswordlessLoginBackend",
    "django.contrib.auth.backends.ModelBackend",
)


# Default region for parsing phone numbers
# Passed as the second argument to python-phonenumbers' .parse
KOMPASSI_PHONENUMBERS_DEFAULT_REGION = "FI"

# Default format for normalizing phone numbers
# getattr'd from phonenumbers.PhoneNumberFormat with itself as default
KOMPASSI_PHONENUMBERS_DEFAULT_FORMAT = "INTERNATIONAL"


# Sending email
if env("EMAIL_HOST", default=""):
    EMAIL_HOST = env("EMAIL_HOST")
else:
    EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="spam@example.com")
GOOGLE_ANALYTICS_TOKEN = env("GOOGLE_ANALYTICS_TOKEN", default="")


if "lippukala" in INSTALLED_APPS:
    import tickets.lippukala_integration

    LIPPUKALA_PREFIXES = tickets.lippukala_integration.PREFIXES
    LIPPUKALA_LITERATE_KEYSPACES = tickets.lippukala_integration.KEYSPACES

    LIPPUKALA_CODE_MIN_N_DIGITS = 7
    LIPPUKALA_CODE_MAX_N_DIGITS = 7

    # NOTE these will be overridden by the respective fields in TicketsEventMeta
    # however, they need to be defined in settings or lippukala will barf.
    LIPPUKALA_PRINT_LOGO_PATH = mkpath("events", "mimicon2016", "static", "images", "mimicon2016_logo.png")
    LIPPUKALA_PRINT_LOGO_SIZE_CM = (3.0, 3.0)


if env("BROKER_URL", default=""):
    CELERY_BROKER_URL = env("BROKER_URL")
else:
    CELERY_TASK_ALWAYS_EAGER = True

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_SEND_TASK_ERROR_EMAILS = not DEBUG
CELERY_SERVER_EMAIL = DEFAULT_FROM_EMAIL

CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_REDIS_SOCKET_KEEPALIVE = True


if "api" in INSTALLED_APPS:
    KOMPASSI_APPLICATION_USER_GROUP = f"{KOMPASSI_INSTALLATION_SLUG}-apps"


if "api_v2" in INSTALLED_APPS:
    AUTHENTICATION_BACKENDS = ("oauth2_provider.backends.OAuth2Backend",) + AUTHENTICATION_BACKENDS

    OAUTH2_PROVIDER = dict(
        SCOPES=dict(
            read="Tietää nimesi, sähköpostiosoitteesi, puhelinnumerosi ja syntymäaikasi",
            write="Muokata käyttäjä- ja henkilötietojasi",
        ),
        PKCE_REQUIRED=False,
    )


if "nexmo" in INSTALLED_APPS:
    NEXMO_USERNAME = env("NEXMO_USERNAME", default="username")
    NEXMO_PASSWORD = env("NEXMO_PASSWORD", default="password")
    NEXMO_FROM = env("NEXMO_FROM", default="358505551234")
    NEXMO_INBOUND_KEY = env("NEXMO_INBOUND_KEY", default="deadbeef")


if env("KOMPASSI_CROWD_APPLICATION_NAME", default=""):
    INSTALLED_APPS = INSTALLED_APPS + ("crowd_integration",)
    KOMPASSI_CROWD_APPLICATION_NAME = env("KOMPASSI_CROWD_APPLICATION_NAME")
    KOMPASSI_CROWD_APPLICATION_PASSWORD = env("KOMPASSI_CROWD_APPLICATION_PASSWORD")
    KOMPASSI_CROWD_HOST = env("KOMPASSI_CROWD_HOST", default="https://crowd.tracon.fi")
    KOMPASSI_CROWD_BASE_URL = f"{KOMPASSI_CROWD_HOST}/crowd/rest/usermanagement/1"


if "desuprofile_integration" in INSTALLED_APPS:
    KOMPASSI_DESUPROFILE_HOST = env("KOMPASSI_DESUPROFILE_HOST", default="https://desucon.fi")
    KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID = env(
        "KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_ID", default="kompassi_insecure_client_id"
    )
    KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_SECRET = env(
        "KOMPASSI_DESUPROFILE_OAUTH2_CLIENT_SECRET",
        default="kompassi_insecure_client_secret",
    )
    KOMPASSI_DESUPROFILE_OAUTH2_SCOPE = ["read"]
    KOMPASSI_DESUPROFILE_OAUTH2_AUTHORIZATION_URL = f"{KOMPASSI_DESUPROFILE_HOST}/oauth2/authorize/"
    KOMPASSI_DESUPROFILE_OAUTH2_TOKEN_URL = f"{KOMPASSI_DESUPROFILE_HOST}/oauth2/token/"
    KOMPASSI_DESUPROFILE_API_URL = f"{KOMPASSI_DESUPROFILE_HOST}/api/user/me/"


KOMPASSI_LISTING_URLCONFS = {
    "conit.fi": "listings.site_urlconfs.conit_fi",
    "animecon.fi": "listings.site_urlconfs.animecon_fi",
}


# Used by access.SMTPServer. Must be created with ssh-keygen -t rsa -m pem (will not work without -m pem).
KOMPASSI_SSH_PRIVATE_KEY_FILE = env(
    "KOMPASSI_SSH_PRIVATE_KEY_FILE", default="/mnt/secrets/kompassi/sshPrivateKey"
)
KOMPASSI_SSH_KNOWN_HOSTS_FILE = env(
    "KOMPASSI_SSH_KNOWN_HOSTS_FILE", default="/mnt/secrets/kompassi/sshKnownHosts"
)

# used by manage.py setup to noop if already run for this deploy
KOMPASSI_SETUP_RUN_ID = env("KOMPASSI_SETUP_RUN_ID", default="")
KOMPASSI_SETUP_EXPIRE_SECONDS = 300


if env("SENTRY_DSN", default=""):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env("SENTRY_DSN", default=""),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )
