from .views import *
from django.urls import path

urlpatterns = [
    path('users/',users_list),
    path('users/<str:pk>/',user_detail),
    path('login/',login),
    path('verify_2fa/',verify_2fa),
    path('forgotPassword/',forgot_password_view),
    path('reset-password/<uuid:token>/', reset_password_view),
]
