# monitor/models.py
from django.db import models

class WaterLevel(models.Model):
    level_cm = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
