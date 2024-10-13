from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Settings(models):
    token = models.CharField(max_length=255)
    api =  models.CharField(max_length=255)
    