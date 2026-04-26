from django.db import models

class Department(models.Model):
    name=models.CharField(max_length=50,primary_key=True)
    def __str__(self):
        return self.name
    
class User(models.Model):
    ROlES=[('ADMIN','admin'),('HR','HR'),('MANAGER','manager')]
    name=models.CharField(max_length=100,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    password=models.CharField(max_length=50)
    role=models.CharField(choices=ROlES)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.name
    
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
