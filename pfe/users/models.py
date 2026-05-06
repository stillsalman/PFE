from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from datetime import timedelta
class Department(models.Model):
    name=models.CharField(max_length=50,primary_key=True)
    def __str__(self):
        return self.name
    
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'admin'
        DDRH = 'HR', 'HR'
        EMPLOYEUR = 'MANAGER', 'manager'
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEUR
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

        # 2FA
    is_2fa_enabled = models.BooleanField(default=False)
    two_factor_code = models.CharField(max_length=6, blank=True, null=True)
    two_factor_expires_at = models.DateTimeField(blank=True, null=True)
    failed_login_attempts = models.IntegerField(default=0)
    lock_until = models.DateTimeField(null=True, blank=True)

    def is_admin_role(self):
        return self.role == self.Role.ADMIN
    def is_ddrh(self):
        return self.role == self.Role.DDRH
    def is_employeur(self):
        return self.role == self.Role.EMPLOYEUR
    def __str__(self):
        return f"{self.username} - {self.role}"
    
class Employee(models.Model):
    name=models.CharField(max_length=100)
    Department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    post=models.CharField(max_length=100)
    telephone=models.IntegerField()
    def __str__(self):
        return self.name
    
class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    message=models.CharField(max_length=150)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # Token expire après 30 minutes
        return not self.is_used and timezone.now() < self.created_at + timedelta(minutes=30)

    def __str__(self):
        return f"Reset token for {self.user.username}"