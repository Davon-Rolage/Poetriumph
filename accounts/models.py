import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    is_premium = models.BooleanField(
        default=False,
        help_text='Designates whether the user is a premium user.'
    )
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        # remove " - deactivated <id>" if exists
        username = self.get_username()
        clean_username = re.sub(r" - deactivated \d+", "", username)
        return f"{clean_username} - ({self.pk})" if clean_username != username else username
        
    
    def save(self, *args, **kwargs):
        if self.is_staff or self.is_superuser:
            self.is_active = True
            
        super().save(*args, **kwargs)


class CustomUserTokenType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class CustomUserToken(models.Model):    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token_type = models.ForeignKey(CustomUserTokenType, on_delete=models.CASCADE)
    expire_date = models.DateTimeField(verbose_name="Token expire date")
    token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.user.get_username() + ' - ' + self.token
    
    def save(self, *args, **kwargs):
        if not self.expire_date:
            self.expire_date = timezone.now() + timezone.timedelta(days=3)
        super().save(*args, **kwargs)

    
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile {self.user.get_username()}'
    
    @property
    def total_poems(self):
        return self.user.poem_set.count()
    