from rest_framework import serializers
from .models import *
class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Training
        fields='__all__'
        
class TrainingNeedSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrainingNeed
        fields='__all__'
        

class DecisionSerializers(serializers.ModelSerializer):
    class Meta:
        model=Decision
        fields='__all__'
        
class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model=TrainingForm
        fields='__all__'