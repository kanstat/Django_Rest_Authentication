from atexit import register
from django.contrib import admin
from django.urls import path

from app1.views import UserRegistrationView
from app1.views import UserLoginView
from app1.views import UserProfileView
from app1.views import UserChangePasswordView
from app1.views import SendPasswordResetToEmailView
from app1.views import UserPasswordResetView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('resetpassword/', SendPasswordResetToEmailView.as_view(),
         name='resetpassword'),
    path('reset-password/<user_id>/<token>/',
         UserPasswordResetView.as_view(), name='reset-password')

]
