from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        field='__all__'