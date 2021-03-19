from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(RequestTalent)
class RequestTalentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'company', 'job_title', 'created_on']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone','created_on']


@admin.register(SubmitJob)
class SubmitJobAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'company', 'job_title', 'job_type', 'created_on']


@admin.register(SubmitCV)
class SubmitCVAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'email', 'phone_number', 'key_skills', 'cv_link', 'created_on']
