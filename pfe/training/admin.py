from django.contrib import admin
from .models import Training,Assignment,Decision,TrainingNeed

admin.site.register(Training)
admin.site.register(Assignment)
admin.site.register(TrainingNeed)
admin.site.register(Decision)