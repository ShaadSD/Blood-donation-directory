from django.db import models
from user.models import User
# Create your models here.

class RewardProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    level = models.CharField(max_length=50, default='Level 1')
    badge = models.CharField(max_length=50, null=True, blank=True)
    


class RewardHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)



    