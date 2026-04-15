from django.db import models
from users.models import User,Employee

class TrainingNeed(models.Model):
    PRIORITY_CHOICES=[('M','must'),('H','have'),('N','need'),('L','low')]
    STATUS_CHOICES=[('S','Submited'),('D','Draft')]
    id=models.BigAutoField(primary_key=True)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    priority=models.CharField(max_length=50,choices=PRIORITY_CHOICES)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Training(models.Model):
    type_training=[('intern','INTERN'),('extern','EXTERN')]
    TrainingNeed_id=models.ForeignKey(TrainingNeed,on_delete=models.CASCADE)
    type=models.CharField(choices=type_training,max_length=50)
    status=models.CharField(max_length=100)
    def __str__(self):
        return self.type
    
class Assignment(models.Model):
    training_id=models.ForeignKey(Training,on_delete=models.CASCADE)
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    start_date=models.DateField()
    end_date=models.DateField()
    def __str__(self):
        return self.training_id
    
class Decision(models.Model):
    TrainingNeed_id=models.ForeignKey(TrainingNeed,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    result=models.CharField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    comment=models.CharField(max_length=200)
    def __str__(self):
        return self.result