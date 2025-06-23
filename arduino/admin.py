# monitor/admin.py

from django.contrib import admin
from .models import WaterLevel

# Register the model
@admin.register(WaterLevel)
class WaterLevelAdmin(admin.ModelAdmin):
    list_display = ('level_cm', 'timestamp')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
