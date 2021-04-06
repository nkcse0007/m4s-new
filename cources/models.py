from django.db import models
from s3upload.fields import S3UploadField
# Create your models here.

from django.utils.translation import ugettext_lazy as _


from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
from rest_framework.exceptions import ValidationError

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

CATEGORY = [
    ('Technology', 'Technology'),
    ('Security', 'Security'),
    ('Certification', 'Certification'),
    ('Government', 'Government'),
    ('Trainings', 'Trainings'),
    ('IT', 'IT')
]


def minimum_length_char(value):
    if len(value) < 2:
        raise ValidationError(
            _('Value should be minimum 3 characters')
        )

LIKE_TYPE = [
    ('LIKE', 'LIKE'),
    ('DISLIKE', 'DISLIKE')
]

def minimum_length_phone(value):
    if len(value) < 7:
        raise ValidationError(
            _('Value should be minimum 3 characters')
        )


class Topic(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, validators=[minimum_length_char],
                            help_text='Name of the Topic')


class Type(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, validators=[minimum_length_char],
                            help_text='Name of the Topic')


class Course(models.Model):
    name = models.CharField(max_length=20, blank=False, null=False, validators=[minimum_length_char],
                            help_text='Name of the Course')
#    image = ArrayField(models.URLField(blank=False, null=False), default=list, blank=False, null=False,
#                       help_text='Add Comma separated multiple image urls')
#    icon = ArrayField(models.URLField(blank=True, null=True), default=list, blank=True, null=True,
#                      help_text='Add Comma separated multiple icon urls')
    image = S3UploadField(dest='example_destination')
    icon = S3UploadField(dest='example_destination')
    category = models.CharField(max_length=20, choices=CATEGORY, blank=False, null=False)
    type = models.ManyToManyField(to=Type, null=True, blank=True)
    topic = models.ManyToManyField(to=Topic, null=True, blank=True)
    is_online=models.BooleanField(default=False)
    in_person = models.BooleanField(default=False)
    brief_description = models.TextField(null=False, blank=False)
    read = models.BooleanField(default=False)
    course_link = models.URLField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the SubmitCV object.
        """
        return str(self.name)


class Comment(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False, help_text='Enter comment')
    user_name = models.CharField(max_length=20, blank=True, null=True, default='',
                                 help_text='Name of user who comment this blog')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the RequestTalent object.
        """
        return str(self.user_name) + ' - ' + str(self.comment)


class CommentReply(models.Model):
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)
    reply = models.TextField(blank=False, null=False, help_text='Enter Reply')
    user_name = models.CharField(max_length=20, blank=False, null=False, help_text='Name of user who comment this blog')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the RequestTalent object.
        """
        return str(self.user_name) + ' - ' + str(self.comment)


class Like(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, blank=True, choices=LIKE_TYPE, null=True, help_text='LIKE or DISLIKE')
    user_name = models.CharField(max_length=20, blank=True, null=True, help_text='Name of user who liked this blog')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the RequestTalent object.
        """
        return str(self.user_name)
