from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'booking/tables', views.BookingViewSet)


urlpatterns = [
    path('', views.index, name="index"),
    re_path(r'^menu-items/?$', views.MenuItemView.as_view(), name="menu-items"),
    path('menu-items/<int:pk>', views.SinlgeMenuItemView.as_view()),
]

urlpatterns += router.urls