from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

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
    telephone = models.CharField(max_length=20, blank=True, null=True)
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
