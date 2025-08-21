from django.contrib import admin
from typing import Any 
from django.contrib.contenttypes.admin import GenericTabularInline 
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _ 

from .models import ContentView

@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display = ["content_object",
     "content_type",
      "user",
      "viewer_ip",
      "last_viewed",
      "created_at",
    ]