from django.db import models

# Create your models here.

class person (models.Model):
    id_name = models.CharField(max_length=50)
    id_age = models.CharField(max_length=50)

class second_model(models.Model):
    task = models.CharField(max_length=50)
    work = models.CharField(max_length=50)