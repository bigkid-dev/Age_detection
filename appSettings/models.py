from django.db import models

# Create your models here.

class Settings(models.Model):
    name = models.CharField(max_length=256, blank=False, default="settings_name")
    value = models.CharField(max_length=256, blank=True, default ="")