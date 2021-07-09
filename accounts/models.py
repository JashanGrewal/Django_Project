from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Contractor(models.Model):
    alphabets = RegexValidator(r'^[a-zA-Z]*$', 'only alphabets are allowed.')
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$','only alphaumeric allowed')
    numeric=RegexValidator(r'^[0-9]*$', 'only numbers allowed')
    name = models.CharField(max_length=30 , validators=[alphabets])
    contactnumber = models.CharField(max_length=10, unique=True,primary_key = True,validators=[numeric])
    gender = models.CharField(max_length=12,validators=[alphabets])
    address = models.CharField(max_length=60,validators=[alphanumeric])
    city = models.CharField(max_length=25 ,validators=[alphabets] )
    state = models.CharField(max_length=12,validators=[alphabets])
    pincode = models.CharField(max_length=6, blank=True, null = True,validators=[numeric])
        
    def __str__(self):
        return self.name 


class labour(models.Model):
    alphabets = RegexValidator(r'^[a-zA-Z]*$', 'only alphabets are allowed.')
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$','only alphaumeric allowed')
    numeric=RegexValidator(r'^[0-9]*$', 'only numbers allowed')
    name = models.CharField(max_length=30 , validators=[alphabets])
    contactnumber = models.CharField(max_length=10, unique=True,primary_key = True,validators=[numeric])
    skills = models.CharField(max_length=20,validators=[alphabets])
    gender = models.CharField(max_length=12,validators=[alphabets])
    address = models.CharField(max_length=60,validators=[alphanumeric])
    city = models.CharField(max_length=25 ,validators=[alphabets] )
    state = models.CharField(max_length=12,validators=[alphabets])
    pincode = models.CharField(max_length=6, blank=True, null = True,validators=[numeric])

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alphabets = RegexValidator(r'^[a-zA-Z ]*$', 'only alphabets are allowed.')
    alphanumeric = RegexValidator(r'^[0-9a-zA-Z ]*$','only alphaumeric allowed')
    numeric=RegexValidator(r'^[0-9]*$', 'only numbers allowed')
    name = models.CharField(max_length=30 , validators=[alphabets])
    contact = models.CharField(max_length=10, unique=True,validators=[numeric],blank=False,null=True)
    gender = models.CharField(max_length=12,validators=[alphabets])
    address = models.CharField(max_length=60,validators=[alphanumeric])
    city = models.CharField(max_length=25 ,validators=[alphabets] )
    state = models.CharField(max_length=12,validators=[alphabets])
    pincode = models.CharField(max_length=6, blank=False, null = True,validators=[numeric])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
