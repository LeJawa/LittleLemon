from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False)
    no_of_guests = models.SmallIntegerField(null=False)
    booking_date = models.DateField(null=False)
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    inventory = models.SmallIntegerField(null=False)
    
    def get_item(self):
        return f'{self.title}: ${str(self.price)}'

    def __str__(self) -> str:
        return self.get_item()

