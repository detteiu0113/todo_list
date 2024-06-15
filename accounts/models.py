from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    # icon = models.ImageField(upload_to='icons/', null=True, blank=True)

    def __str__(self):
        return self.username