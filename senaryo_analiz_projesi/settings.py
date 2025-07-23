

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-s%v-(m@75f*===dx@5bp#&uh__+1^tx6juustn+(y@88w9_7*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Yüklenen kullanıcı dosyaları (PDF'ler, resimler vb.) için ayarlar
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Statik dosyalar (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'analiz_uygulamasi', 'static'),
]

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages', # Mesaj framework'ü için gerekli
    'django.contrib.staticfiles',
    'analiz_uygulamasi',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', # Mesaj framework'ü için gerekli
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'senaryo_analiz_projesi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], # Boş bırakılabilir, APP_DIRS True olduğu için
        'APP_DIRS': True, # Uygulamaların templates klasörlerini aramasını sağlar
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug', # Debug modu için
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages', # Mesajları şablona iletir
            ],
        },
    },
]

WSGI_APPLICATION =  'senaryo_analiz_projesi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


JAZZMIN_SETTINGS = {
    "site_title": "Senaryo Analiz Admin",
    "site_header": "Senaryo Analiz",
    "site_brand": "Senaryo AI",
    "site_logo": "admin/img/logo.png", # Varsayılan logo yolu, isterseniz kendi logonuzu koyabilirsiniz
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "welcome_sign": "Senaryo Analiz Paneline Hoş Geldiniz",
    "copyright": "Melis Yıldırım - 2025",
    "search_model": ["auth.User", "auth.Group"], # Admin panelinde arama yapılabilecek modeller
    "topbar_links": [
        {"name": "Dış Bağlantı", "url": "https://ai.google.dev/gemini-api", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["analiz_uygulamasi", "auth"], # Uygulamaların sıralaması
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "vertical_tabs", "auth.group": "vertical_tabs"},
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "flatly", # Jazzmin teması (flatly, cosmo, lumen, etc.)
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    }
}