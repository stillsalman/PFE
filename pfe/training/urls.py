from django.urls import path
from .views import *
urlpatterns = [
    path('training-needs/', get_training_needs),
]
