from django.contrib import admin

from .models import *


# Register your models here.


@admin.register(ReferFriend)
class ReferFriendAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'company', 'job_type', 'job_title', 'created_on']
