from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate 
from django.utils import timezone
from datetime import timedelta
import random
from django.core.mail import send_mail
from django.conf import settings
 
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
        return Response({"message": "Username and password required"}, status=400)

    user = User.objects.filter(username=username).first()

    if not user:
        return Response({"message": "Invalid credentials"}, status=401)

    # 🔒 blocked check
    if user.lock_until and timezone.now() < user.lock_until:
        return Response({"message": "Account locked. 2FA required to unlock."}, status=403)

    user_auth = authenticate(username=username, password=password)

    # ❌ WRONG PASSWORD
    if user_auth is None:
        user.failed_login_attempts += 1

        # 🚨 LOCK + TRIGGER 2FA ONLY HERE
        if user.failed_login_attempts >= 3:
            user.lock_until = timezone.now() + timedelta(minutes=5)
            user.failed_login_attempts = 0

            # generate 2FA ONLY when locked
            code = str(random.randint(100000, 999999))
            user.two_factor_code = code
            user.two_factor_expires_at = timezone.now() + timedelta(minutes=5)

            print(f"2FA code for {user.username}: {code}")

        user.save()
        return Response({"message": "Invalid credentials"}, status=401)

    # ✅ CORRECT PASSWORD
    user.failed_login_attempts = 0
    user.lock_until = None

    # ❌ IMPORTANT CHANGE:
    # DO NOT trigger 2FA here anymore

    user.save()

    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        }
    })
 
@api_view(['GET','POST'])
@permission_classes([AllowAny])#IsAdminRole
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
@permission_classes([AllowAny])#IsAdminRole
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
@permission_classes([AllowAny])#IsAuthenticated
def get_notification(request):
    try:
        user=User.objects.get(pk=request.data.get('pk'))
    except User.DoesNotExist:
        return Response({"message": "user does not exist!"},error=400)
    notif=Notification.objects.filter(user=user)
    serializer=NotificationSerializer(notif,many=True)
    return Response(serializer.data)
@api_view(['PATCH'])
@permission_classes([AllowAny])#IsAuthenticated
def is_read(request,pk):
    try:
        note=Notification.objects.get(pk=pk)
    except Notification.DoesNotExist:
        return Response({"message": "notification does not exist"},status=400)
    note.is_read=True
    note.save()
    return Response({"message": "notification status changed"})


@api_view(["POST"])
@permission_classes([AllowAny])
def verify_2fa(request):
    user_id = request.data.get("user_id")
    code = request.data.get("code")

    if not user_id or not code:
        return Response({"message": "user_id and code required"}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    # ❌ expired check
    if not user.two_factor_expires_at or timezone.now() > user.two_factor_expires_at:
        return Response({"message": "Code expired"}, status=400)

    # ❌ wrong code
    if user.two_factor_code != code:
        return Response({"message": "Invalid code"}, status=400)

    # ✅ UNLOCK ACCOUNT
    user.lock_until = None
    user.failed_login_attempts = 0
    user.two_factor_code = None
    user.two_factor_expires_at = None

    user.save()

    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Account unlocked & login successful",
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role,
        }
    })
    

@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password_view(request):
    email = request.data.get("email")

    if not email:
        return Response(
            {"message": "L'adresse email est obligatoire."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        
        return Response(
            {"message": "Si cet email existe, un lien de réinitialisation a été envoyé."},
            status=status.HTTP_200_OK
        )

    # Invalider les anciens tokens de ce user
    PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)

    # Créer un nouveau token
    reset_token = PasswordResetToken.objects.create(user=user)

    # lien frontend
    reset_link = f"{settings.FRONTEND_URL}/reset-password/{reset_token.token}"

    # Envoyer l'email
    send_mail(
        subject="Réinitialisation de votre mot de passe",
        message=f"Bonjour {user.first_name},\n\nCliquez sur ce lien pour réinitialiser votre mot de passe :\n{reset_link}\n\nCe lien expire dans 30 minutes.\n\nSi vous n'avez pas demandé cette réinitialisation, ignorez cet email.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=['raoufassam74@gmail.com'],
    )
    print('code: ',reset_token.token)

    return Response(
        {"message": "Si cet email existe, un lien de réinitialisation a été envoyé."},
        status=status.HTTP_200_OK
    )
    






@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password_view(request, token):
    new_password = request.data.get("new_password")

    if not new_password:
        return Response(
            {"message": "New password required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        return Response({"message": "Invalid token."}, status=400)

    if not reset_token.is_valid():
        return Response({"message": "Token expired or already used."}, status=400)

    user = reset_token.user

    user.set_password(new_password)

    # reset security state
    user.failed_login_attempts = 0
    user.lock_until = None
    user.two_factor_code = None
    user.two_factor_expires_at = None
    user.save()

    reset_token.is_used = True
    reset_token.save()

    return Response({"message": "Password reset successful."}, status=200)