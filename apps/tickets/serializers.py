from rest_framework import serializers

from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    state = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ('id', 'title', 'description', 'author', 'state')

    def get_state(self, instance):
        return instance.state


class TicketStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = ('state',)
