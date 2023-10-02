from django.db import models

class Booking(models.Model):
    Name = models.CharField(max_length=255, null=False)
    No_of_guests = models.SmallIntegerField(null=False)
    BookingDate = models.DateField(null=False)
    
class Menu(models.Model):
    Title = models.CharField(max_length=255, null=False)
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    Inventory = models.SmallIntegerField(null=False)


