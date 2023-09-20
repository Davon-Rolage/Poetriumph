from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_premium = models.BooleanField(
        default=False,
        help_text='Designates whether the user is a premium user.'
    )
    is_active = models.BooleanField(
        default=False
    )
    token = models.CharField(max_length=36, blank=True)
    
    def __str__(self):
        return self.username
    
    
class MyProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    poem_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
    
    