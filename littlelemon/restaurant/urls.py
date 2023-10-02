from django.urls import path, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'booking/tables', views.BookingViewSet)
router.register(r'show/menu-items', views.ShowMenuItemViewSet, basename="show_menuitem")
router.register(r'manage/menu-items', views.ManageMenuItemView, basename="manage_menuitem")


urlpatterns = [
    
]

urlpatterns += router.urls