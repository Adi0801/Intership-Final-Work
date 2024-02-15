from django.db import models
from django.http import request
from django.contrib.auth import get_user_model

User=get_user_model()

class profile(models.Model):
    username=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.TextField()
    last_name=models.TextField()
    location=models.CharField(max_length=100, blank=True)
    age=models.IntegerField()
    bio=models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    request = models.TextField(blank=True)
    sent_date = models.DateField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateField(auto_now_add=False, null=True, blank=True)
    timeslot = models.CharField(max_length=20,default="Unknown")
    doctor = models.CharField(max_length=100,default="Unknown")

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ["-sent_date"]