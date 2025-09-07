from django.contrib import admin
from core.models import TimestampedModel


@admin.register(TimestampedModel)

class TimestampModelAdmin(admin.ModelAdmin):
    list_display = ['created_at', "updated_at"]
