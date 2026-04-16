from .views import *
from django.urls import path

urlpatterns = [
    path('users/',users_list),
    path('users/<str:pk>/',user_detail),
    path('login/',login)
]
