import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DEBUG = env.bool('DEBUG', False)

SECRET_KEY = env.str('SECRET_KEY', 'django-insecure-vpo7n#p+n_333j@2dy6$&8tibp*sll(x#$*6_7a!3!uc^cibb*')

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

if env.str('DB_CONNECTION','sqlite3') == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            }
            }
elif env.str('DB_CONNECTION') == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.{}'.format(env.str('DB_CONNECTION', 'mysql')),
            'NAME': env.str('DB_DATABASE', 'zdac'),
            'USER': env.str('DB_USERNAME', 'zdac'),
            'PASSWORD': env.str('DB_PASSWORD', ''),
            'HOST': env.str('DB_HOST', 'localhost'),
            'PORT': env.int('DB_PORT', 3306),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
                'use_unicode': True,
            },
        }
    }

INSTALLED_APPS = (['database', 'rest_framework'])

LANGUAGE_CODE = 'pt-BR'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = False
