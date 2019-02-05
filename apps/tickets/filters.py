from django_filters import rest_framework as filters

from .models import Ticket


class UserStatisticFilterSet(filters.FilterSet):
    date_start = filters.DateFilter(field_name='created', lookup_expr='gte')
    date_end = filters.DateFilter(field_name='created', lookup_expr='lte')
    performer = filters.NumberFilter(field_name='performer_id')

    class Meta:
        model = Ticket
        fields = ('performer', 'date_start', 'date_end')
