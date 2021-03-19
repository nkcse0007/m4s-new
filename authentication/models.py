from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from authentication.Controller.managers.user import ManagerAccountUser
from datetime import datetime

CUSTOMER = 'CUSTOMER'
USER_ROLES = [
    (CUSTOMER, 'CUSTOMER')
]


def minimum_length_char(value):
    if len(value) < 3:
        raise ValidationError(
            _('Value should be minimum 3 characters'),
            params={'value': value},
        )


def minimum_length_phone(value):
    if len(value) < 7:
        raise ValidationError(
            _('Value should be minimum 3 characters'),
            params={'value': value},
        )


class Permissions(models.Model):
    """
    Create Permissions
    """

    title = models.CharField(max_length=20, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class User(AbstractBaseUser, PermissionsMixin):
    """
    Create Users with role
    """

    groups = None
    user_permissions = None
    email = models.EmailField(unique=True, help_text='Email of user', blank=False, null=False)
    user_name = models.CharField(max_length=20, blank=True, default='',
                                 help_text='User Name of user')
    name = models.CharField(max_length=50, blank=False, null=False, validators=[minimum_length_char],
                            help_text='Name of user')
    phone = models.CharField(max_length=13, blank=True, validators=[minimum_length_phone], default='',
                             help_text='Phone number of user')
    role = models.CharField(max_length=20, choices=USER_ROLES, blank=False, null=False, help_text='Role of user')
    permissions = models.ManyToManyField(to=Permissions, help_text='Permission of user')
    status = models.BooleanField(default=True, help_text='User is active, blocked or not')
    zone = models.CharField(max_length=20, blank=True, default='N/A')
    address = models.TextField(blank=True, default='')
    city = models.CharField(max_length=20, blank=True, default='')
    state = models.CharField(max_length=20, blank=True, default='')
    country = models.CharField(max_length=20, blank=True, default='')
    pin = models.CharField(max_length=6, blank=True, default='')

    is_active = \
        models.BooleanField(default=True,
                            help_text="Toggles active status for a user.")

    is_staff = models.BooleanField(default=False,
                                   help_text="Designates the user as "
                                             "a staff member.")

    is_superuser = models.BooleanField(default=False,
                                       help_text="Designates the user as"
                                                 " a super user.")
    is_verified = models.BooleanField(default=True,
                                      help_text="Toggles verification status for a user.")

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    objects = ManagerAccountUser()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the user object.
        """
        return str(self.name) + ' ' + str(self.email)


class JwtToken(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    jwtId = models.TextField(blank=False)
    expiresIn = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.jwtId
