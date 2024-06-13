from django.db import models
from accounts.models import CustomUser

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title