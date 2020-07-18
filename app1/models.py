from django.db import models
from datetime import datetime
from django.conf import settings

class User(models.Model):
    user_first_name=models.CharField(max_length=50,null=False)
    user_last_name=models.CharField(max_length=50,null=False)   
    user_email=models.EmailField(primary_key=True,null=False)
    user_DOB=models.DateField(null=False)
    user_password=models.CharField(max_length=100,null=False)
    user_Codechef_id=models.CharField(max_length=50,null=True)
    user_Codeforces_id=models.CharField(max_length=50,null=True)
    is_admin=models.BooleanField(default=False)
    user_join_date=models.DateTimeField(auto_now_add=True)
    user_post=models.CharField(max_length=50,default="user")
    user_profile_photo=models.ImageField(upload_to="profile/",null=True)

class Notification(models.Model):
    notofication_topic=models.CharField(max_length=50)
    notofication_content=models.CharField(max_length=1000)
    notofication_datetime=models.DateTimeField(auto_now_add=True)
    notification_seen=models.ManyToManyField(User)

class Event(models.Model):
    event_name=models.CharField(max_length=50)
    event_start_date=models.DateTimeField(null=False)
    event_end_date=models.DateTimeField(null=False)
    event_details=models.CharField(max_length=5000)
    event_registation=models.CharField(max_length=1000,default="")
    
class Event_Photos(models.Model):
    event_id=models.ForeignKey(Event,on_delete=models.CASCADE)
    event_photo=models.ImageField(upload_to="event_photos/",null=True)

class Resources(models.Model):
    resource_name=models.CharField(max_length=50)
    resource_content=models.CharField(max_length=500)
    resource_link=models.CharField(max_length=5000, default="")
    resource_date_time=models.DateTimeField(null=False,default=datetime.now())
# Create your models here.
