from django.urls import path
from .views import *
urlpatterns = [
    path('training-needs/', post_training_needs),
    path('training-needs/<int:pk>', update_training_need),
    path('trainings',get_trainings),
    path('DDRH/decesion/<int:pk>',make_decesion),
    path('export/training-needs/', Generate_report),
    path('DDRH/form', get_post_forms),
    path('form',manager_form),
    path('DDRH/submitedForms',access_submited_forms),
    path('DDRH/submitedForms/<int:pk>',manage_submited_forms),
    ]
