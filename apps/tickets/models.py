from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Prefetch
from django_fsm import FSMField, transition, can_proceed, has_transition_perm

from tickets.helpers import user_is_performer, can_processed, user_is_author


class Ticket(models.Model):
    ASSIGNED_TICKETS_NAME = 'assigned_tickets'
    SELF_TICKETS_NAME = 'self_tickets'

    title = models.CharField(max_length=255)
    description = models.TextField()
    state = FSMField(default='new')
    author = models.ForeignKey(
        get_user_model(),
        related_name=SELF_TICKETS_NAME,
        on_delete=models.SET_NULL,
        null=True
    )
    performer = models.ForeignKey(
        get_user_model(),
        related_name=ASSIGNED_TICKETS_NAME,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tickets'

    @transition('state', source=('new', 'reopened'), target='assigned')
    def assigned(self):
        """Назначаем пользователя с наименьшем количеством тикетов"""
        users = get_user_model().objects.prefetch_related(
            Prefetch(self.ASSIGNED_TICKETS_NAME, self.__class__.objects.filter(state__in=('assigned', 'processed')))
        )
        self.performer_id = sorted(
            [(user.id, user.assigned_tickets.count()) for user in users],
            key=lambda item: item[1]
        )[0][0]

    @transition(
        'state',
        source='assigned',
        target='processed',
        permission=user_is_performer,
        conditions=[can_processed]
    )
    def processed(self):
        """
        Перевод тикета в состояние "обрабатывается" только если
        текущий пользователь назначен на тикет исполнителем
        """

    @transition('state', source='processed', target='successed', permission=user_is_performer)
    def successed(self):
        """Выполнение тикета"""

    @transition('state', source='processed', target='canceled', permission=user_is_performer)
    def canceled(self):
        """Отмена тикета"""

    @transition('state', source=('canceled', 'successed'), target='closed', permission=user_is_author)
    def closed(self):
        """Закрытие тикета"""

    @transition('state', source=('canceled', 'successed'), target='reopened', permission=user_is_author)
    def reopened(self):
        """Переоткрытие тикета"""

    def change_state(self, state, user):
        state_method = getattr(self, state)
        if can_proceed(state_method) and has_transition_perm(state_method, user):
            state_method()
            self.save()

    def __str__(self):
        return self.title
