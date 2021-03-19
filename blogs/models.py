import jsonfield
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.

CATEGORY = [
    ('TECHNOLOGIES', 'TECHNOLOGIES'),
    ('TIPS', 'TIPS'),
    ('NEWS', 'NEWS'),
    ('INTERVIEWS', 'INTERVIEWS'),
    ('LEARNING', 'LEARNING'),
    ('TRAINING', 'TRAINING')
]

BLOG_TYPE = [
    ('NEWS', 'NEWS'),
    ('INTERVIEW_TIPS', 'INTERVIEW_TIPS'),
    ('CAREER_DEVELOPMENT', 'CAREER_DEVELOPMENT')
]

LIKE_TYPE = [
    ('LIKE', 'LIKE'),
    ('DISLIKE', 'DISLIKE')
]


def reply_check(value):
    if type(value) is not dict:
        raise ValidationError(
            _('Value is not dict'),
            params={'value': value},
        )


class Blog(models.Model):
    type = models.CharField(max_length=20, choices=BLOG_TYPE, blank=False, null=False)
    heading = models.TextField(blank=False, null=False, help_text='Add Heading of Blog')
    image = ArrayField(models.URLField(blank=False, null=False), default=list, blank=False, null=False, help_text='Add Comma separated multiple image urls')
    icon = ArrayField(models.URLField(blank=True, null=True), default=list, blank=True, null=True, help_text='Add Comma separated multiple icon urls')
    category = models.CharField(max_length=20, choices=CATEGORY, blank=False, null=False)
    small_description = models.TextField(null=False, blank=False)
    detailed_description = models.TextField(null=False, blank=False)
    date = models.DateTimeField(blank=True, null=True)
    author = models.CharField(blank=True, null=True, max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # ---------------------------------------------------------------------------
    def __str__(self):
        """
        Returns the string representation of the RequestTalent object.
        """
        return str(self.category) + ' - ' + str(self.heading)


class Comment(models.Model):
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
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
    blog = models.ForeignKey(to=Blog, on_delete=models.CASCADE)
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
