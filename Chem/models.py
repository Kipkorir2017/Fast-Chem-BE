from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE)
        name = models.CharField(max_length=500, blank=True)
        profile_pic = models.ImageField(upload_to = 'images/')
        location=models.CharField(max_length=200, blank=True)
        contact = models.CharField(max_length=30, blank=True)
    
# class medicine(models.Model):
#     name = models.CharField(max_length=50)
#     price = models.DecimalField(max_digits=10)
#     pharmacyName=models.CharField(max_length=50)
#     location=models.CharField(max_length=50)

class Pharmacy(models.Model):
    name=models.CharField(max_length=50)
    location=models.CharField(max_length=50)
    medicine_name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10)
    