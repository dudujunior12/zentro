from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from api.models import Categories, Tickets

class AdminTests(APITestCase):
    def setUp(self):
        self.category = Categories.objects.create(name='Infraestructure')
        self.requester = User.objects.create_user(username='requester1', password='123')
        admin_group = Group.objects.get_or_create(name='Admins')[0]
        self.admin = User.objects.create_user(username='adminuser', password='123')
        self.admin.groups.add(admin_group)

        # Criar vários tickets
        Tickets.objects.create(title='Chamado 1', description='A', category=self.category, created_by=self.requester)
        Tickets.objects.create(title='Chamado 2', description='B', category=self.category, created_by=self.requester)

        # Login como admin via token
        response = self.client.post('/api/token/', {
            'username': 'adminuser',
            'password': '123',
        }, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_admin_sees_all_tickets(self):
        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 2)
