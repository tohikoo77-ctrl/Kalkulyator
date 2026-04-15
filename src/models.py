from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Calculator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)

    expression = models.CharField(max_length=255, verbose_name='ifoda')
    result = models.CharField(max_length=255, verbose_name='natija')

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}: {self.expression} = {self.result}"



