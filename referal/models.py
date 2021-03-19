from django.db import models

# Create your models here.


JOB_TYPE = [
    ('PART TIME', 'PART TIME'),
    ('FULL TIME', 'FULL TIME')
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


class ReferFriend(models.Model):
    first_name = models.CharField(max_length=20, blank=False, null=False, validators=[minimum_length_char], help_text='First Name of employer')
    last_name = models.CharField(max_length=20, blank=True, null=True, help_text='Last Name of employer')
    email = models.EmailField(blank=False, null=False, help_text='Email Id of employer')
    phone_number = models.CharField(max_length=13, blank=False, null=False, validators=[minimum_length_phone])
    company = models.CharField(max_length=30, blank=False, null=False, help_text='Company Name of employer')
    job_title = models.CharField(max_length=30, blank=False, null=False, help_text='Job Title of job')
    job_type = models.TextField(blank=True, choices=JOB_TYPE, null=True, help_text='Job Type')
    job_description = models.TextField(blank=True, null=True, help_text='Job Description of job')
    job_location = models.CharField(max_length=30,  blank=False, null=False)
    roles_and_responsiblities = models.TextField(blank=False, null=False)
    experience_requirement = models.TextField(blank=True, null=True)
    skill_and_certification = models.TextField(blank=True, null=True)
    id_link = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the RequestTalent object.
        """
        return str(self.first_name) + '  ' + str(self.email)
