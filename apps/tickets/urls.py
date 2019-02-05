from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TicketViewSet, UserStatisticViewSet

router = DefaultRouter()
router.register('tickets', TicketViewSet, basename='tickets')
router.register('statistic', UserStatisticViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('statistic/', UserStatisticViewSet)
]