from rest_framework import serializers
from django.contrib.auth.models import User

from .models import MenuItem, Booking

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['email']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        
class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Booking
        fields = ['user', 'name', 'no_of_guests', 'booking_date']
    