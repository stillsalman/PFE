from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        permissions = validated_data.pop('user_permissions', [])
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        if groups:
            user.groups.set(groups)
        if permissions:
            user.user_permissions.set(permissions)

        return user
        
        
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employee
        field='__all__'
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        field='__all__'