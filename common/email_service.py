from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_simple_email(data):
    """
    Send email to the admin.
    """
    email = data.get("email")
    message = data.get("message", '')
    name = data.get("name", '')
    file = data.get("file", None)
    message = "My name is {0} and my email is {1} and my query is {2}".format(name, email, message)
    msg = EmailMessage(
        'Contact Email',
        message,
        "contact@4actuaries.com",
        ['contact@4actuaries.com'],
    )
    if file:
        msg.attach(file.name, file.read(), file.content_type)
    msg.send()


def send_template_email(data):
    """
    Sends the activation/cancellation subscription mail to the user.
    """

    subject = data.get('subject', '')
    html_content = data.get('template', '')
    to = data.get('to', '')
    message = data.get('message', '')

    msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
