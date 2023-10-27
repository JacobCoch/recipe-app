from django.urls import path
from .views import Profile

app_name = "users"

urlpatterns = [
    path('profile/<slug:username>/', Profile.as_view(), name='profile'),
]
