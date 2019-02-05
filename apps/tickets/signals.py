from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django_fsm.signals import post_transition

from .models import Ticket


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_transition, sender=Ticket)
@receiver(post_save, sender=Ticket)
def assign_ticket(sender, instance, **kwargs):
    if kwargs.get('created') or kwargs.get('target') == 'reopened':
        instance.change_state('assigned', instance.author)
