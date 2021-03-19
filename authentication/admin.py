from django.contrib import admin
from authentication.models import User, Permissions, JwtToken
from authentication.Controller.user_admin import FormAccountUserAdmin
from authentication.Controller.user_change import FormAccountUserChange
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = FormAccountUserChange
    add_form = FormAccountUserAdmin

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'phone', 'created_on')
    list_filter = ()
    # readonly_fields = ["email"]
    fieldsets = (
        ('Authentication', {'fields': ('email', 'password',)}),
        ("Personal Details", {'fields': (
             'name', "phone",)}),
        ('Other Information', {'fields': (
            'role', 'permissions', 'status', 'is_verified',
        )}),
        ('Address', {'fields': (
            'zone', 'address', "city", 'state',
            'country', 'pin',
        )})
    )
    # # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        ('Authentication', {
            'classes': ('wide',),
            'fields': ('email', 'password',)}),
        ("Personal Details", {
            'classes': ('wide',),
            'fields': (
                'user_name', 'name', "phone",)}),
        ('Other Information', {
            'classes': ('wide',),
            'fields': (
                'role', 'permissions', 'status', 'is_verified',
            )}),
        ('Address', {
            'classes': ('wide',),
            'fields': (
                'zone', 'address', "city", 'state',
                'country', 'pin',
            )})
    )
    search_fields = ('email', 'name')
    ordering = ('created_on',)
    filter_horizontal = ()


admin.site.unregister(Group)


@admin.register(Permissions)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(JwtToken)
class JwtTokenAdmin(admin.ModelAdmin):
    list_display = ['jwtId', 'expiresIn', 'created_on', 'updated_on']
