from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
 
 
@api_view(['POST'])
def login(request):
     serializer=UserSerializer(data=request.data, partial=True)
     if(serializer.is_valid()):
         email=serializer.validated_data['email']
         password=serializer.validated_data['password']
         try:
             user=User.objects.get(email=email,password=password)
             return Response({"msg": "congragulation!!"})
         except User.DoesNotExist:
             return Response({"msg": "failled to log you in"}, status=status.HTTP_403_FORBIDDEN)
         
     return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['GET','POST'])
def users_list(request):
    if request.method == 'GET':
        #handle get request
        users=User.objects.all()
        serializer= UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method =='POST':
        #handle posr request
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','PATCH','DELETE'])
def user_detail(request,pk):
    
    try:
        user= User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'user not found'}, status=404)
    
    if request.method=='GET':
        serializer=UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method=='PATCH':
        serializer=UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        user.delete()
        return Response({"message": "user deleted"}, status=204)

@api_view(['GET'])
def get_notification(request,pk):
    try:
        user=User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({"message": "user does not exist!"},error=400)
    notif=Notification.objects.filter(user=user)
    serializer=NotificationSerializer(notif,many=True)
    return Response(serializer.data)