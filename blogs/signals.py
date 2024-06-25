from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from .models import Blog, Subscribe
from django.conf import settings


@receiver(post_save, sender=Blog)
def newsletter_send_mail(sender, instance, created, **kwargs):
    email_list = Subscribe.objects.values_list("email", flat=True)
    if created and email_list:
        send_mail(
            "Blogger",
            "Have you read our new blogs?",
            settings.EMAIL_HOST_USER,
            email_list,
            fail_silently=True
        )
