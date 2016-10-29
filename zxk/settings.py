"""
Django settings for zxk project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e1a)^i!apr6#qw0e_7gl=uj+(9^7t9c0-auncutsub7(-b2!n!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #'account',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.sitemaps',

    'home',
    'blog',
    'accounts',
    'images',
    #'actions',
    'pagedown',
]

# account 使用Django自带认证系统，使用这个时urls中就不要用namespace了
# accounts 自定义的认证系统

SITE_ID = 1


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zxk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'zxk.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zxk',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'common_static'),
]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Email setting
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = os.environ.get("MAIL_USERNAME")
EMAIL_HOST_PASSWORD = os.environ.get("MAIL_PASSWORD")
# EMAIL_HOST_PASSWORD = "qucibejzibqebhcb"
EMAIL_PORT = 25
EMAIL_USE_TLS = True

# 上面的配置是通过SMTP发送邮件，下面的是让邮件发送到终端
# you can configure Django to write e-mails to the standard output instead 
# of sending them through an SMTP server. Django provides an e-mail backend 
# to write e-mails to the console.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Django authentication views

# The reverse_lazy() function reverses URLs just like reverse() does, 
# but you can use it when you need to reverse URLs before your 
# project's URL configuration is loaded.

from django.core.urlresolvers import reverse_lazy

# Tells Django which URL to redirect after login
# if the contrib.auth.views.login view gets no next parameter
LOGIN_REDIRECT_URL = reverse_lazy('accounts:profile')

# Is the URL to redirect the user to log in (e.g. using the
# login_required decorator)
LOGIN_URL = reverse_lazy('accounts:login')

# Is the URL to redirect the user to log out
LOGOUT_URL = reverse_lazy('accounts:logout')


# User Model
#...


# AUTHENTICATION_BACKENDS = (
#     'social.backends.github.GithubOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# )




# Social Auth

# github

# 为了使用http也可以，否则会报错
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


# upper

CLIENT_ID= '9890f2416a5ee83e8da8'
CLIENT_SECRET = '9ad5f139646112dd848a295b1b708730fe4152f2'

AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'

RECIRECT_URI = "http://127.0.0.1:8000/accounts/github-auth"
SCOPE = []


# 为每个用户对象添加url，具体解释见 accounts/views.py
ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: reverse_lazy('accounts:user_detail', args=[u.username]),
}

# pagedown settings
PAGEDOWN_SHOW_PREVIEW = True
#PAGEDOWN_WIDGET_TEMPLATE = 'blog/pagedown.html'
#PAGEDOWN_WIDGET_CSS = ('blog/pagedown.css',)
#PAGEDOWN_EXTENSIONS = []