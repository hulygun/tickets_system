from django.conf import settings
from django.db import models
from django_fsm import FSMField, transition, can_proceed


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    state = FSMField(default='new')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='self_tickets',
        on_delete=models.SET_NULL,
        null=True
    )
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tickets',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tickets'

    @transition('state', source='new', target='assigned')
    def assigned(self):
        self.description = 'it s assign!'

    @transition('state', source='assigned', target='processed')
    def processed(self):
        pass

    def change_state(self, state):
        if can_proceed(getattr(self, state)):
            self.state = state
            getattr(self, state)()
            self.save()
        else:
            raise Exception
