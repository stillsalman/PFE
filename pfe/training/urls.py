from django.urls import path
from .views import *
urlpatterns = [
    path('training-needs/', get_post_training_needs),
    path('training-needs/<int:pk>', update_training_need),
    path('trainings',get_trainings),
    path('training-response',training_response),
    path('decesion/<int:pk>',make_decesion)
    ]
