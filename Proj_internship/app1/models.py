from django.db import models


# Create your models here.
class Info(models.Model):
    DoesNotExist = None
    objects = None
    S_ID = models.IntegerField(max_length=5).primary_key
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Password = models.CharField(max_length=8)
