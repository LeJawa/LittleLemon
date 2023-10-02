from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from restaurant.models import MenuItem


class MenuViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        MenuItem.objects.create(title="IceCream", price=2, inventory=100)
        MenuItem.objects.create(title="Pasta", price=9, inventory=26)
        MenuItem.objects.create(title="Salad", price=8, inventory=34)
    
    def test_getall(self):
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'IceCream')
        self.assertContains(response, 'Pasta')
        self.assertContains(response, 'Salad')