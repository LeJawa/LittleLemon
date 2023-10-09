from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = DefaultRouter()

router.register(r'user/reservation/tables', views.UserBookingViewSet, basename="user_booking")
router.register(r'staff/reservation/tables', views.StaffBookingViewSet, basename="staff_booking")
router.register(r'show/menus', views.ShowMenuViewSet, basename="show_menu")
router.register(r'manage/menus', views.ManageMenuView, basename="manage_menu")


urlpatterns = [    
    path('api-token-auth/', obtain_auth_token), # Only for assignment purposes. Token can be obtained via djoser endpoints.
]

urlpatterns += router.urls