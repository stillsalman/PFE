from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate 
 
class IsDDRH(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.DDRH
        )
        
class IsEmployeur(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.EMPLOYEUR
        )

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )
 
 
 
 
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response(
            {
                "message": "Le nom d'utilisateur et le mot de passe sont obligatoires."
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    user = authenticate(username=username, password=password)
    if user is None:
        return Response(
            {
                "message": "Nom d'utilisateur ou mot de passe incorrect."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "message": "Connexion rÃ©ussie.",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        },
        status=status.HTTP_200_OK
    )
 
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