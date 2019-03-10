"""
Django settings for MxOnline project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '4kx2yw388f91+gyr8mgj^s&1mqade&hmz0urkkev&v1y&p%o_3'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
# ALLOWED_HOSTS = ['*']
DEBUG = True
ALLOWED_HOSTS = []


# Application definition
AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'courses',
    'organization',
    'operation',
    'xadmin',
    'crispy_forms',
    'captcha',
    'pure_pagination',
    'DjangoUeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'users.UserProfile'

ROOT_URLCONF = 'MxOnline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'MxOnline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'mxonline',
    #     'USER': 'root',
    #     'PASSWORD': '0000',
    #     'HOST': '127.0.0.1'
    # },

}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = 'static'   # 新增行
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, '/static/'),   # 修改
)


# EMAIL_HOST = 'smtp.163.com'    # 'smtp.qq.com'
# EMAIL_PORT = 25
# EMAIL_HOST_USER = '15735177116@163.com'   # '1271570224@qq.com' # 你的邮箱账号
# EMAIL_HOST_PASSWORD = '1234567890qwerty'  # 'xmdmlixvyyezhbge'  # 这里是邮箱提供给的授权码，不是个人密码
# EMAIL_USE_TLS = True   # 保持不变
# EMAIL_FROM = '15735177116@163.com'  # '1271570224@qq.com'  # 你的邮箱账号

EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = '1271570224@qq.com' # 你的邮箱账号
EMAIL_HOST_PASSWORD = 'xmdmlixvyyezhbge'  # 这里是邮箱提供给的授权码，不是个人密码
EMAIL_USE_TLS = True   # 保持不变
EMAIL_FROM = '1271570224@qq.com'  # 你的邮箱账号

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



