from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created_on']


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Topic)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['name']
