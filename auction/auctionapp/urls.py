from django.urls import path
from .views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('signup/', UserRegistrationView.as_view(), name='signup')
]
