from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

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
        ticket.change_state(serializer.data.get('state'))

        return Response(self.get_serializer(ticket).data)

