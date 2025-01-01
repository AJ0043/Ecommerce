from django.test import TestCase

# Create your tests here.
from django.core.mail import send_mail
from django.conf import settings

send_mail(
    'Test Subject',
    'This is a test email.',
    'techstech506@gmail.com',  # From email
    ['recipient@example.com'],  # To email
    fail_silently=False,
)

