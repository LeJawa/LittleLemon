from django.test import TestCase
from restaurant.models import MenuItem

class MenuItemTest(TestCase):
    def test_get_item(self):
        title = "IceCream"
        price = 2
        
        item = MenuItem.objects.create(title=title, price=price, inventory=100)
        itemstr = item.get_item()
        
        self.assertEqual(itemstr, f"{title}: ${price}")