from django.db import models

class Department(models.Model):
    name=models.CharField(max_length=50,primary_key=True)
    def __str__(self):
        return self.name

class User(models.Model):
    ROlES=[('ADMIN','admin'),('HR','HR'),('manager','MANAGER')]
    name=models.CharField(max_length=100,primary_key=True)
    email=models.EmailField(max_length=100)
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