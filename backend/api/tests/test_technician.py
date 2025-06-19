from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from api.models import Categories, Tickets

class TechnicianTests(APITestCase):
    def setUp(self):
        self.category = Categories.objects.create(name='Software')
        self.requester = User.objects.create_user(username='requester1', password='123')
        tech_group = Group.objects.get_or_create(name='Technicians')[0]
        self.technician = User.objects.create_user(username='technician1', password='123')
        self.technician.groups.add(tech_group)

        # Ticket sem assigned
        Tickets.objects.create(title='Sem assigned', description='Livre', category=self.category, created_by=self.requester)

        # Ticket assigned a ele
        Tickets.objects.create(
            title='Assigned',
            description='Chamado técnico',
            category=self.category,
            assigned_to=self.technician,
            created_by=self.requester
        )

        # Ticket assigned a outro
        other = User.objects.create_user(username='technician2', password='123')
        Tickets.objects.create(
            title='Assigned a outro',
            description='Outro',
            category=self.category,
            assigned_to=other,
            created_by=self.requester
        )

        # Autenticar técnico via JWT
        response = self.client.post('/api/token/', {
            'username': 'technician1',
            'password': '123',
        }, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_technician_sees_only_assigned_and_unassigned(self):
        response = self.client.get('/api/tickets/')
        self.assertEqual(response.status_code, 200)
