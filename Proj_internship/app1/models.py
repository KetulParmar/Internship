from django.db import models


# Create your models here.
class Info(models.Model):
    objects = None
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Password = models.CharField(max_length=8)
