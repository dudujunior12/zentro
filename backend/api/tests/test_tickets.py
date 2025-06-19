from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from api.models import Categories, Tickets

class TicketTests(APITestCase):
    def setUp(self):
        self.category = Categories.objects.create(name='Hardware')

        group = Group.objects.get_or_create(name='Requester')[0]
        self.requester = User.objects.create_user(username='requester1', password='123')
        self.requester.groups.add(group)

        # Obter token JWT
        response = self.client.post('/api/token/', {
            'username': 'requester1',
            'password': '123',
        }, format='json')

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_ticket(self):
        response = self.client.post('/api/tickets/', {
            'title': 'Problema no teclado',
            'description': 'Teclado não funciona',
            'category': self.category.id
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['created_by'], self.requester.id)
        
    def test_requester_can_only_see_own_tickets(self):
        other_user = User.objects.create_user(username='requester2', password='123')
        Tickets.objects.create(
            title='Outro chamado',
            description='Chamado de outro usuário',
            category=self.category,
            created_by=other_user
        )

        # Criar ticket do requester
        Tickets.objects.create(
            title='Meu chamado',
            description='Chamado do requester',
            category=self.category,
            created_by=self.requester
        )

        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['created_by'], self.requester.id)
