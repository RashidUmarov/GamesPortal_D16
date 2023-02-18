from django.urls import path
from .views import UserProfile, subscribe, unsubscribe

urlpatterns = [
    path('<int:pk>', UserProfile.as_view(), name='profile'),
    path('subscribe/', subscribe, name='subscribe'),
    path('unsubscribe/', unsubscribe, name='unsubscribe'),
]
