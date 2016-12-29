"""
Django settings for AllStars project.

Generated by 'django-admin startproject' using Django 1.9.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6!)5-*-&azs8)4jdepx@gmcqhh65e*w93u18s3g^hw9fhq&b(p'

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'djoser',
    'corsheaders',
    'import_export',
    'constance',
    'constance.backends.database',
]

PROJECT_APPS = [
    'activities',
    'categories',
    'employees',
    'stars',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + PROJECT_APPS

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    # Rules to block users
    'MAX_STARS_GIVEN_DAY': (10, 'Maximum number of points given by one employee daily'),
    'MAX_STARS_RECEIVED_DAY': (15, 'Maximum number of points received to employee daily'),
    'MAX_STARS_GIVEN_MONTHLY': (30, 'Maximum number of points given by one employee in a month'),
    'MAX_STARS_RECEIVED_MONTHLY': (45, 'Maximum number of points received to one employee in a month'),

    # Email errors messages
    'EMAIL_DOMAIN_FORBIDDEN': ('Email domain %s is forbidden.', 'Error message when email domain is not in email domain list'),
    'EMAIL_SERVICE_ERROR': ('There are problems with email service, please contact an administrator.', 'Error message when email service is not available.'),
    'INVALID_EMAIL_ADDRESS': ('%s is not a valid email address.', 'Error message when email address is invalid.'),

    # Categories messages
    'KEYWORD_ALREADY_EXISTS': ('Data already exists or is invalid.', 'Error message when a keyword already exists or is not set.'),
    'CATEGORY_BAD_REQUEST': ('Bad request on creation or edition category, please review if category already exists.', 'Error message when a category can not be added or edited.'),

    # User messages
    'EMPLOYEE_CREATION_SUBJECT': ('[BELATRIX CONNECT] Your account has been successfully created.', 'Email subject when new account is created.'),
    'EMPLOYEE_CREATION_MESSAGE': ('Your username is: %s and your initial random password is %s', 'Email message when new account is created'),
    'EMPLOYEE_RESET_PASSWORD_CONFIRMATION_SUBJECT': ('[BELATRIX CONNECT] Please confirm if you want a password reset.', 'Confirmation reset password email subject.'),
    'EMPLOYEE_RESET_PASSWORD_CONFIRMATION_MESSAGE': ('If you want to reset your password please confirm the request, clicking here: %s', 'Confirmation reset password email message.'),
    'EMPLOYEE_RESET_PASSWORD_SUCCESSFULLY_SUBJECT': ('[BELATRIX CONNECT] Your new password has been successfully created.', 'Reset password successfully email subject '),
    'EMPLOYEE_RESET_PASSWORD_SUCCESSFULLY_MESSAGE': ('Your new password is: %s', 'Reset password successfully email message.'),
    'USER_EMAIL_ALREADY_REGISTERED': ('email %s is already registered.', 'Error message when user already exists.'),
    'USER_SUCCESSFULLY_CREATED': ('User(s) successfully created.', 'Message when an account has been created successfully.'),
    'USER_SUCCESSFULLY_CREATED_EMAIL_ERROR': ('User was created, but there are problems with email service, please contact an administrator.', 'Message when an account has been created successfully but no email was sent.'),
    'USER_SUCCESSFULLY_RESET_PASSWORD': ('Successfully password creation, email has been sent.', 'Successfully user reset password.'),
    'USER_UNABLE_TO_LOG': ('User is unable to log in with provided credentials.', 'Error message when user are not able to log in'),
    'USER_LOGOUT': ('User logout successfully', 'Message when user logout'),
    'USER_DATA_IS_MISSING': ('User data is missing', 'Message when user data update is missing'),
    'TOP_LIST_EMPTY': ('Top list is empty', 'Message when top list is empty'),

    # Password errors messages
    'PASSWORD_EQUAL': ('New and current password are equal', 'Error message when new and current password are equal.'),
    'WRONG_CURRENT_PASSWORD': ('Current password is wrong.', 'Error message when current password is wrong.'),

    # Administrator errors messages
    'SET_LIST_TYPE_UNKNOWN': ('Field type unknown', 'Error message when field type is unknown'),

    # Stars messages
    'SUCCESSFULLY_STARS_ADDED': ('Successfully points added', 'Successfully message when bulk points added.'),
    'USER_BLOCKED_TO_GIVE_STARS': ('User is blocked to give recommendations. Please contact your project leader.', 'Error message when user is blocked to give recommendations.'),
    'USER_BLOCKED_TO_RECEIVED_STARS': ('User is blocked to received recommendations.', 'Error message when user is blocked to received recommendations.'),
    'USER_UNABLE_TO_GIVE_STARS_ITSELF': ('User is unable to give recommendations to itself.', 'Error message when user is unable to give recommendations to itself.'),
    'NO_STARS_RECEIVED': ('No recommendations yet.', "Message when user doesn't have recommendations yet."),

    # Daily cron tasks messages
    'DAILY_EXECUTION_CONFIRMATION_SUBJECT': ('[BELATRIX CONNECT] Daily check has been executed.', 'Email confirmation subject for daily tasks.'),
    'DAILY_EXECUTION_CONFIRMATION_MESSAGE': ('Your daily check scores and rules has been executed.', 'Email confirmation message for daily tasks.'),
    'DAILY_EXECUTION_CONFIRMATION_EMAIL': ('sergio@neosergio.net', 'Email address to send daily message for daily tasks.'),
    'USER_BLOCKED_NOTIFICATION_SUBJECT': ('[BELATRIX CONNECT] Your user account is blocked in BELATRIX CONNECT', 'Email notificacion subject when user is blocked'),
    'USER_BLOCKED_NOTIFICATION_MESSAGE': ('Your username %s is blocked. Please contact with your project leader for more details.', 'Email notificacion message when user is blocked'),

    # Activities messages
    'NO_MESSAGE': ('Message is empty.', 'Error message when message is empty'),
    'TITLE_PUSH_NOTIFICATION': ('BELATRIX Connect', 'Title for push notifications'),
    'LEVEL_UP_TEXT': ('%s %s achieved level %d.', 'Message when user level up.'),
    'RECOMMENDATION_MESSAGE': ('You earn %d point(s), %s %s gives you a recommendation', 'Message when user receives a recommendation'),
    'ROLE_AUTHORIZED': ('Notifier', 'Role authorized to send push notification messages'),
}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AllStars.urls'

# SWAGGER
SWAGGER_SETTINGS = {
    "api_version": '0.1',
    "is_authenticated": True
}

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = ('GET',
                      'POST',
                      'PUT',
                      'PATCH',
                      'DELETE',
                      'OPTIONS')
CORS_ALLOW_HEADERS = ('x-requested-with',
                      'content-type',
                      'accept',
                      'origin',
                      'authorization',
                      'x-csrftoken',
                      'accept-enconding',
                      'accept-language')
CORS_EXPOSE_HEADERS = ('Access-Control-Allow-Origin',
                       'Access-Control-Allow-Headers')

# REST
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# USER MODEL
AUTH_USER_MODEL = "employees.Employee"
NEXT_LEVEL_SCORE = 25

# DJOSER
DJOSER = {
    'DOMAIN': 'belatrixsf.com',
    'SITE_NAME': 'Belatrix All Stars',
    'SET_PASSWORD_RETYPE': False,
}

# EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_DOMAIN_LIST = {
    'belatrixsf.com',
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AllStars.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {}
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__ + '/../../'))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

# Push Notifications
FIREBASE_API_URL = 'https://fcm.googleapis.com/fcm/send'
