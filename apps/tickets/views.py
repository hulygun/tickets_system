from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from tickets.filters import UserStatisticFilterSet
from .models import Ticket
from .serializers import TicketSerializer, TicketStateSerializer


class TicketViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    """Докстринг для эндпоинта тикетов"""
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()

    def get_serializer_class(self):
        return self.serializer_class if not self.action == 'change_state' else TicketStateSerializer

    def create(self, request, *args, **kwargs):
        """Докстринг создания тикета"""
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['put'])
    def change_state(self, request, *args, **kwargs):
        ticket = self.get_object()
        serializer = self.get_serializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        ticket.change_state(request.data.get('state'), request.user)

        return Response(self.get_serializer(ticket).data)


class UserStatisticViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Докстринг статистики тикетов по пользователям"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserStatisticFilterSet
    queryset = Ticket.objects.all()

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).values('state').annotate(
            cnt=Count('state')
        ).values('state', 'cnt')
        return Response(queryset)
