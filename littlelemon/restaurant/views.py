from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Menu, Booking
from .serializers import MenuSerializer, UserBookingSerializer, StaffBookingSerializer

def index(request):
    return render(request, 'index.html', {})
def menu(request):
    return render(request, 'menu.html', {})
def bookings(request):
    return render(request, 'booking.html', {})
def users(request):
    return render(request, 'users.html', {})

class ManageMenuView(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminUser,]

class ShowMenuViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class UserBookingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Booking.objects.all()
    serializer_class = UserBookingSerializer
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class StaffBookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = StaffBookingSerializer
    permission_classes = [IsAdminUser,]