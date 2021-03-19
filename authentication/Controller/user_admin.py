from django import forms
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.urls import reverse
from django.utils.safestring import mark_safe
from authentication.models import User, Permissions


class FormAccountUserAdmin(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control required', 'placeholder': 'email'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control required',
                                                         'placeholder': 'Name'}))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control required',
                                                                                   'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('email', "name",)

        # ---------------------------------------------------------------------------
        # clean_email
        # ---------------------------------------------------------------------------


    def clean_email(self):
        """
        Makes sure that the email being registered is unique
        """

        email = self.cleaned_data['email']

        try:
            existing_user = User.objects.get(email=email)
            # self.login_url = reverse('authentication:login')

            if existing_user.is_active:
                raise ValidationError(mark_safe('An account already exists with'
                                                ' this email. Please login instead'))
            else:
                raise ValidationError(mark_safe('This account is disabled. '
                                                'Please contact support.'))

        except ObjectDoesNotExist:
            pass

        return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user