from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import MenuItem, Booking
from .serializers import MenuItemSerializer, BookingSerializer

def index(request):
    return render(request, 'index.html', {})
def menu(request):
    return render(request, 'menu.html', {})
def bookings(request):
    return render(request, 'booking.html', {})
def users(request):
    return render(request, 'users.html', {})

class ManageMenuItemView(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser,]

class ShowMenuItemViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class UserBookingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class StaffBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser,]