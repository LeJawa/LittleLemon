from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from restaurant.models import Booking

from warnings import filterwarnings
from django.core.paginator import UnorderedObjectListWarning

filterwarnings('ignore', category=UnorderedObjectListWarning)

class BookingViewTest(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username='testuser1', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass')
        self.user3 = User.objects.create_user(username='testuser3', password='testpass')
        self.staff = User.objects.create_user(username='teststaff', password='testpass', is_staff=True) 
        
        Booking.objects.create(user=self.user1, title="Birthday Party", no_of_guests=10, booking_date='2023-10-01')   
        Booking.objects.create(user=self.user1, title="Date", no_of_guests=2, booking_date='2023-10-03')         
        Booking.objects.create(user=self.user2, title="Family Reuniony", no_of_guests=5, booking_date='2023-10-02')   
        Booking.objects.create(user=self.user3, title="Farewell Party", no_of_guests=13, booking_date='2023-10-01')   
    
    def login_as_staff(self):
        self.token = Token.objects.create(user=self.staff)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def login_as_user1(self):
        self.token = Token.objects.create(user=self.user1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def login_as_user2(self):
        self.token = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
    def login_as_user3(self):
        self.token = Token.objects.create(user=self.user3)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    

class UserBookingViewTest(BookingViewTest):
    
    def test_list_only_users_bookings(self):
        self.login_as_user1()
        
        response = self.client.get(reverse('user_booking-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Birthday Party')
        self.assertContains(response, 'Date')
        self.assertNotContains(response, 'Family Reunion')
        self.assertNotContains(response, 'Farewell Party')
        
        self.login_as_user2()
        
        response = self.client.get(reverse('user_booking-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotContains(response, 'Birthday Party')
        self.assertNotContains(response, 'Date')
        self.assertContains(response, 'Family Reunion')
        self.assertNotContains(response, 'Farewell Party')
    
    def test_retrieve_as_user(self):
        self.login_as_user1()        
        booking = Booking.objects.create(user=self.user1, title="Professional Meal", no_of_guests=6, booking_date='2023-10-05')
        Booking.objects.create(user=self.user1, title="Regular", no_of_guests=1, booking_date='2023-10-01')
        
        response = self.client.get(reverse('user_booking-detail', args=[booking.id]))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Professional Meal')
        self.assertNotContains(response, 'Regular')
    
    def test_create_as_user(self):
        self.login_as_user1()        
        previous_count = Booking.objects.count()
        
        response = self.client.post(reverse('user_booking-list'), data={'user': self.user1.id, 'title': 'Regular', 'no_of_guests': 1, 'booking_date': '2023-10-01'})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), previous_count + 1)
        self.assertEqual(Booking.objects.get(title='Regular').no_of_guests, 1)
        
    def test_delete_as_user(self):
        self.login_as_user1()        
        previous_count = Booking.objects.count()
        booking = Booking.objects.create(user=self.user1, title="Professional Meal", no_of_guests=6, booking_date='2023-10-05')
        
        response = self.client.delete(reverse('user_booking-detail', args=[booking.id]))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), previous_count)
        
    def test_unauthorized_methods(self):
        self.login_as_user1()    
        response = self.client.put(reverse('user_booking-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        response = self.client.patch(reverse('user_booking-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_authentication_required(self):        
        response = self.client.get(reverse('user_booking-list'))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
class StaffBookingViewTest(BookingViewTest):  
    def test_list_all_bookings_as_staff(self):
        self.login_as_staff()
        
        response = self.client.get(reverse('staff_booking-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Birthday Party')
        self.assertContains(response, 'Date')
        self.assertContains(response, 'Family Reunion')
        self.assertContains(response, 'Farewell Party')
    
    def test_retrieve_as_staff(self):
        self.login_as_staff()        
        booking = Booking.objects.create(user=self.user1, title="Professional Meal", no_of_guests=6, booking_date='2023-10-05')
        Booking.objects.create(user=self.user1, title="Regular", no_of_guests=1, booking_date='2023-10-01')
        
        response = self.client.get(reverse('staff_booking-detail', args=[booking.id]))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Professional Meal')
        self.assertNotContains(response, 'Regular')
    
    def test_create_as_staff(self):
        self.login_as_staff()        
        previous_count = Booking.objects.count()
        
        response = self.client.post(reverse('staff_booking-list'), data={'user': self.user1.id, 'title': 'Regular', 'no_of_guests': 1, 'booking_date': '2023-10-01'})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), previous_count + 1)
        self.assertEqual(Booking.objects.get(title='Regular').no_of_guests, 1)
        
    def test_delete_as_staff(self):
        self.login_as_staff()        
        previous_count = Booking.objects.count()
        booking = Booking.objects.create(user=self.user1, title="Professional Meal", no_of_guests=6, booking_date='2023-10-05')
        
        response = self.client.delete(reverse('staff_booking-detail', args=[booking.id]))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), previous_count)
        
    def test_update_as_staff(self):
        self.login_as_staff()        
        booking = Booking.objects.create(user=self.user1, title="Professional Meal", no_of_guests=6, booking_date='2023-10-05')
        
        response = self.client.patch(reverse('staff_booking-detail', args=[booking.id]), data={'no_of_guests': 3})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Booking.objects.get(id=booking.id).no_of_guests, 3)
        
    def test_staff_required(self):        
        response = self.client.get(reverse('staff_booking-list'))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        self.login_as_user1()        
        response = self.client.get(reverse('staff_booking-list'))
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)