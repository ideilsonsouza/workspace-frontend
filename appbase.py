import sys

sys.dont_write_bytecode = True

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django

django.setup()

import settings
from settings import env

from data.models import *

