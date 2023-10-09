from django.test import TestCase, Client
from restaurant.models import Menu, Booking, User

class MenuTest(TestCase):
    def test_get_item(self):
        title = "IceCream"
        price = 2
        
        item = Menu.objects.create(title=title, price=price, inventory=100)
        itemstr = item.get_item()
        
        self.assertEqual(itemstr, f"{title}: ${price}")
        
class BookingTest(TestCase):    
    def test_get_booking(self):
        title = "Reunion"
        no_of_guests = 10
        booking_date = "2021-03-04"
        user = User.objects.create_user(username='testuser', password='testpass')
        
        
        booking = Booking.objects.create(user=user, title=title, no_of_guests=no_of_guests, booking_date=booking_date)
        bookingstr = booking.get_booking()
        
        self.assertEqual(bookingstr, f'{title} ({booking_date}): ${str(no_of_guests)}')