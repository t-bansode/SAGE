from django.contrib import admin

# Register your models here.
from .models import Story

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'created_at')
    search_fields = ('topic', 'user__username')
