import random
import string

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TicketFlowTests(APITestCase):
    user_password = None

    def setUp(self):
        # Создаём рандомный пароль
        self.user_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # Генерируем тестовых юзеров
        for i in range(3):
            setattr(self, 'user_{}'.format(i), get_user_model().objects.create_user(
                username='user_{}'.format(i),
                email='user{}@localhost.local'.format(i),
                password=self.user_password
            ))

    def test_ticket_created(self):
        url = reverse('tickets-list')
        data = {'title': 'Тикет', 'description': 'Описание'}
        response1 = self.client.post(url, data, format='json')
        # Проверяем, что неавторизованный юзер не может создать тикет
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
        # Авторизуем юзера по токену и проверим, что он может создать тикет
        self._authorize('user_1')
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def _authorize(self, user):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + getattr(self, user).auth_token.key)

