from rest_framework import serializers
from django.contrib.auth.models import User

from .models import MenuItem, Booking

class UserSerializer(serializers.ModelSerializer):   
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CurrentUserSerializer(serializers.ModelSerializer): 
    is_staff = serializers.SerializerMethodField(read_only=True)
   
    class Meta:
        model = User
        fields = ['username', 'is_staff']
    
    def get_is_staff(self, user: User):
        return user.is_staff

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = "__all__"
        
class UserBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Booking
        fields = ['id', 'user', 'title', 'no_of_guests', 'booking_date']
        read_only_fields = ['user']
        
    def create(self, validated_data):
        user = self.context['request'].user
        booking = Booking.objects.create(user=user, **validated_data)
        return booking
        
class StaffBookingSerializer(serializers.ModelSerializer):
    user = UserSerializer
    class Meta:
        model = Booking
        fields = ['id', 'user', 'title', 'no_of_guests', 'booking_date']
    