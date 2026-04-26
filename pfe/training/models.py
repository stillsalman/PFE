from django.db import models
from users.models import User



class TrainingForm(models.Model):
    from_status=[('DRAFT','draft'),('SENT','sent')]
    manager=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)
    finalDate=models.DateField()
    status=models.CharField(max_length=50,choices=from_status, default='DRAFT')
    def __str__(self):
        return str(self.manager)

class TrainingNeed(models.Model):
    PRIORITY_CHOICES=[('M','must'),('N','need'),('L','low')]
    form=models.ForeignKey(TrainingForm,on_delete=models.CASCADE)
    STATUS_CHOICES=[('APPROVED','approved'),('DENIED','denied'),('WAITING','waiting')]
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=200)
    priority=models.CharField(max_length=50,choices=PRIORITY_CHOICES)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='WAITING')
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title



class Training(models.Model):
    type_training=[('intern','INTERN'),('extern','EXTERN')]
    status_choices=[('assigned','ASSIGNED'),('notassigned','NOTASSIGNED')]
    title=models.CharField(max_length=100)
    TrainingNeed=models.ForeignKey(TrainingNeed,on_delete=models.CASCADE)
    type=models.CharField(choices=type_training,max_length=50)
    status=models.CharField(max_length=100,choices=status_choices,default='notassigned')
    def __str__(self):
        return self.type
    
  
class Decision(models.Model):
    STATUS_CHOICES=[('APPROVED','approved'),('DENIED','denied')]
    TrainingNeed=models.ForeignKey(TrainingNeed,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    result=models.CharField(max_length=100,choices=STATUS_CHOICES)
    date=models.DateTimeField(auto_now_add=True)
    comment=models.CharField(max_length=200)
    def __str__(self):
        return self.result