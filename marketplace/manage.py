"""
Django settings for marketplace project.
"""
 
from pathlib import Path
from datetime import timedelta
 
BASE_DIR = Path(__file__).resolve().parent.parent
 
# ---------------------------------------------------------------------------
# Segurança
# ---------------------------------------------------------------------------
# ATENÇÃO: em produção, mova para variável de ambiente (.env)
SECRET_KEY = "django-insecure-1ep_ei96n900rmy4ts1e_of)=y@y9fmj8rwu3i8edfrkwaunb5"
 
DEBUG = True
 
ALLOWED_HOSTS = []
 
# ---------------------------------------------------------------------------
# Apps
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # terceiros
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",  # necessário para logout
    "corsheaders",
    # nossos apps
    "accounts",
    "stores",
    "products",
    "core",
]
 
# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",          # deve ser o primeiro
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
 
ROOT_URLCONF = "marketplace.urls"
 
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
 
WSGI_APPLICATION = "marketplace.wsgi.application"
 
# ---------------------------------------------------------------------------
# Banco de dados
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
 
# ---------------------------------------------------------------------------
# Usuário customizado
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"
 
# ---------------------------------------------------------------------------
# Autenticação JWT
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
 
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}
 
# ---------------------------------------------------------------------------
# CORS (Vite dev server)
# ---------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
 
# ---------------------------------------------------------------------------
# Validação de senha
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
 
# ---------------------------------------------------------------------------
# Internacionalização
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True
 
# ---------------------------------------------------------------------------
# Arquivos estáticos e de mídia
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
 
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
 
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
 
