from django.db import models


# Create your models here.
class Question(models.Model):
    question = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
