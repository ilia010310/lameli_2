from apps.about.models import CallBack
from django.contrib import admin


@admin.register(CallBack)
class CallBAckAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'created']
    ordering = ['id']
