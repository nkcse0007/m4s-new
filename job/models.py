from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your models here.

EXPERIENCE_PERIOD = [
    ('DAY', 'DAY'),
    ('MONTH', 'MONTH'),
    ('YEAR', 'YEAR')
]

EXPERIENCE_LEVEL = [
    ('0 - 2 YEARS', '0 - 2 YEARS'),
    ('2 - 5 YEARS', '2 - 5 YEARS'),
    ('5 - 10 YEARS', '5 - 10 YEARS'),
    ('10 - 15 YEARS', '10 - 15 YEARS'),
    ('15+ YEARS', '15+ YEARS'),
]

SALARY_BUDGET = [
    ('0 - 2 Lakh per anum', '0 - 2 Lakh per anum'),
    ('2 - 5 Lakh per anum', '2 - 5 Lakh per anum'),
    ('5 - 10 Lakh per anum', '5 - 10 Lakh per anum'),
    ('10 - 20 Lakh per anum', '10 - 20 Lakh per anum'),
    ('>20 Lakh per anum', '>20 Lakh per anum')
]

JOB_TYPE = [
    ('PART TIME', 'PART TIME'),
    ('FULL TIME', 'FULL TIME')
]

SECTOR = [
    ('GOVERNMENT', 'GOVERNMENT'),
    ('PRIVATE', 'PRIVATE')
]


def minimum_length_char(value):
    if len(value) < 2:
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


class RequestTalent(models.Model):
    first_name = models.CharField(max_length=20, blank=False, null=False, validators=[minimum_length_char],
                                  help_text='First Name of employer')
    last_name = models.CharField(max_length=20, blank=True, null=True, help_text='Last Name of employer')
    email = models.EmailField(blank=False, null=False, help_text='Email Id of employer')
    company = models.CharField(max_length=30, blank=False, null=False, help_text='Company Name of employer',
                               validators=[minimum_length_char])
    job_title = models.CharField(max_length=30, blank=False, null=False, help_text='Job Title of job',
                                 validators=[minimum_length_char])
    job_description = models.TextField(blank=True, null=True, help_text='Job Description of job')
    job_location = models.CharField(max_length=30, blank=False, null=False, validators=[minimum_length_char])
    budget_from = models.IntegerField(blank=True, null=True)
    budget_to = models.IntegerField(blank=True, null=True)
    experience_from = models.IntegerField(blank=True, null=True)
    experience_to = models.IntegerField(blank=True, null=True)
    experience_period = models.CharField(max_length=20, choices=EXPERIENCE_PERIOD, blank=True, null=True)
    expected_joining_date = models.DateTimeField(blank=True, null=True)
    open_positions = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=False, null=False, validators=[minimum_length_phone])
    help_text = models.TextField(blank=False, null=False, validators=[minimum_length_char])
    attachment_link = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the RequestTalent object.
        """
        return str(self.first_name) + '  ' + str(self.email)


class SubmitJob(models.Model):
    first_name = models.CharField(max_length=20, blank=False, null=False, validators=[minimum_length_char],
                                  help_text='First Name of employer')
    last_name = models.CharField(max_length=20, blank=True, null=True, help_text='Last Name of employer')
    email = models.EmailField(blank=False, null=False, help_text='Email Id of employer')
    company = models.CharField(max_length=30, blank=False, null=False, help_text='Company Name of employer',
                               validators=[minimum_length_char])
    job_title = models.CharField(max_length=30, blank=False, null=False, help_text='Job Title of job',
                                 validators=[minimum_length_char])
    phone_number = models.CharField(max_length=13, blank=False, null=False, validators=[minimum_length_phone])
    job_type = models.TextField(blank=False, choices=JOB_TYPE, null=False, help_text='Job Type')
    remote_job = models.BooleanField(default=False)
    sector = models.CharField(max_length=30, choices=SECTOR, blank=True, null=True)
    job_location = models.CharField(max_length=30, blank=False, null=False)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL, null=False, blank=False)
    salary_budget = models.CharField(max_length=40, choices=SALARY_BUDGET, null=False, blank=False)
    job_description = models.TextField(blank=True, null=True, help_text='Job Description of job')
    roles_and_responsiblities = models.TextField(blank=False, null=False)
    experience_requirement = models.TextField(blank=True, null=True)
    skill_and_certification = models.TextField(blank=True, null=True)
    jd_link = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the SubmitJob object.
        """
        return str(self.first_name) + '  ' + str(self.email)


class SubmitCV(models.Model):
    first_name = models.CharField(max_length=20, blank=False, null=False, validators=[minimum_length_char],
                                  help_text='First Name of employer')
    last_name = models.CharField(max_length=20, blank=True, null=True, help_text='Last Name of employer')
    email = models.EmailField(blank=False, null=False, help_text='Email Id of employer')
    phone_number = models.CharField(max_length=13, blank=False, null=False, validators=[minimum_length_phone])
    key_skills = ArrayField(models.CharField(max_length=50, blank=True, null=True), default=list, blank=True, null=True,
                            help_text='Enter multiple key skills with comma separated.')
    additional_info = models.TextField(blank=True, null=True)
    cv_link = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the SubmitCV object.
        """
        return str(self.first_name) + '  ' + str(self.email)


class ContactUs(models.Model):
    """
    Model: Contact us page data
    description: Contact us information
    """
    name = models.CharField(max_length=250, help_text="Enter name.", blank=False, null=False)
    email = models.EmailField(help_text="Enter email", blank=False, null=False)
    phone = models.CharField(max_length=13, null=False, blank=False)
    message = models.TextField(help_text="Enter your message", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ContactForm"
        verbose_name_plural = "ContactForm"

    def __str__(self):
        """
        return _str_
        """
        return self.email

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        mail_subject = 'User Wants to contact.'
        message = render_to_string('contactus.html', {
            'user': self,
        })
        to_email = self.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        try:
            email.send()
        except Exception as e:
            print(e.__str__())

        return super(ContactUs, self).save()
