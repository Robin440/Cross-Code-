from django.contrib import admin
from core.models import TimestampedModel
from django.contrib.auth.models import Group, Permission


@admin.register(TimestampedModel)
# @admin.site.register(Group)
# @admin.site.register(Permission)

class TimestampModelAdmin(admin.ModelAdmin):
    list_display = ['created_at', "updated_at"]
