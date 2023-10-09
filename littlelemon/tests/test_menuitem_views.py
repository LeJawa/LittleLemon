from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from restaurant.models import MenuItem

class MenuItemViewTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.staff = User.objects.create_user(username='teststaff', password='testpass', is_staff=True)   
        
        MenuItem.objects.create(title="Ice Cream", price=2, inventory=100)
        MenuItem.objects.create(title="Pasta", price=9, inventory=26)
        MenuItem.objects.create(title="Salad", price=8, inventory=34)    
    
    def login_as_staff(self):
        self.token = Token.objects.create(user=self.staff)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def login_as_user(self):
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

class ShowMenuItemViewTest(MenuItemViewTest):
    
    def test_list_as_anon(self):
        response = self.client.get(reverse('show_menuitem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Ice Cream')
        self.assertContains(response, 'Pasta')
        self.assertContains(response, 'Salad')
    
    def test_retrieve_as_anon(self):
        menu_item1 = MenuItem.objects.create(title="Ice Cream", price=2, inventory=100)
        MenuItem.objects.create(title="Pasta", price=2, inventory=100)
        response = self.client.get(reverse('show_menuitem-detail', args=[menu_item1.id]))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Ice Cream')
        self.assertNotContains(response, 'Pasta')
    
    def test_unauthorized_methods(self):
        response = self.client.post(reverse('show_menuitem-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.put(reverse('show_menuitem-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(reverse('show_menuitem-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.delete(reverse('show_menuitem-list'))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
class ManageMenuItemViewTest(MenuItemViewTest):
    
    def test_list_as_staff(self):
        self.login_as_staff()
        
        response = self.client.get(reverse('manage_menuitem-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Ice Cream')
        self.assertContains(response, 'Pasta')
        self.assertContains(response, 'Salad')
    
    def test_retrieve_as_staff(self):
        self.login_as_staff()        
        menu_item = MenuItem.objects.create(title="Pizza", price=12, inventory=100)
        MenuItem.objects.create(title="Steak", price=20, inventory=100)
        
        response = self.client.get(reverse('manage_menuitem-detail', args=[menu_item.id]))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Pizza')
        self.assertNotContains(response, 'Steak')
    
    def test_create_as_staff(self):
        self.login_as_staff()        
        previous_count = MenuItem.objects.count()
        
        response = self.client.post(reverse('manage_menuitem-list'), data={'title': 'Pizza', 'price': 12, 'inventory': 100})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MenuItem.objects.count(), previous_count + 1)
        self.assertEqual(MenuItem.objects.get(title='Pizza').price, 12)
        
    def test_destroy_as_staff(self):
        self.login_as_staff()        
        previous_count = MenuItem.objects.count()
        menu_item = MenuItem.objects.create(title="Pizza", price=12, inventory=100)
        
        response = self.client.delete(reverse('manage_menuitem-detail', args=[menu_item.id]))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MenuItem.objects.count(), previous_count)
        
    def test_update_as_staff(self):
        self.login_as_staff()        
        menu_item = MenuItem.objects.create(title="Chicken Nuggets", price=2, inventory=100)
        
        response = self.client.patch(reverse('manage_menuitem-detail', args=[menu_item.id]), data={'price': 3})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MenuItem.objects.get(title='Chicken Nuggets').price, 3)
        
    def test_unauthorized_as_user_or_anon(self):
        response = self.client.get(reverse('manage_menuitem-list'))        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.login_as_user()
        
        response = self.client.get(reverse('manage_menuitem-list'))        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    