from django.contrib import admin

from .models import Paste

@admin.register(Paste)
class PasteAdmin(admin.ModelAdmin):
    list_display = ('paste_time', 'slug', 'title', 'viewcount', 'paste_ip')
