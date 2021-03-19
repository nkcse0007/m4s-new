from django.contrib import admin

from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget
from .models import *


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['type', 'heading', 'category', 'created_on']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'comment', 'user_name', 'created_on']
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user_name', 'created_on']

# Register your models here.
