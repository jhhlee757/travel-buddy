from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postdata):
        errors = {}
        filterusername = User.objects.filter(username = postdata['username'])
        if len(postdata['name']) < 3:
            errors['name'] = "Name must be at least 3 characters"
        if len(postdata['username']) < 3:
            errors['username']= "Username must be at least 3 characters"
        if len(filterusername) > 0:
            errors['username'] = "This username is already taken"
        if len(postdata['password']) < 6:
            errors['password'] = "Password must be atleast 6 characters"
        if postdata['confirmpw'] != postdata['password']:
            errors['confirmpw'] = "Password not confirmed"
        return errors

    def validator2(self, postdata):
        errors = {}
        filterusername = User.objects.filter(username = postdata['username'])
        if len(filterusername) == 0:
            errors['username'] = "Invalid Username"
        else:
            usertocheck = filterusername[0]
            if not bcrypt.checkpw(postdata['password'].encode(), usertocheck.password.encode()):
                errors['password'] = "Invalid password"
        return  errors
    
    def validator3(self, postdata):
        time = datetime.now()
        errors = {}
        if len(postdata['dest']) < 1:
            errors['dest'] = "Title cannot be empty"
        if len(postdata['desc']) < 1:
            errors['desc'] = "Description cannot be empty"
        if postdata['travel_from'] < str(time):
            errors['travel_from'] = "Start date cannot be in the past"
        if postdata['travel_to'] < postdata['travel_from']:
            errors['travel_to'] = "End date must be after start date"
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    travel_start_date = models.DateField()
    travel_end_date = models.DateField()
    plan = models.TextField()
    creator = models.ForeignKey(User, related_name = "trips_created", on_delete = models.CASCADE)
    participants = models.ManyToManyField(User, related_name = "trips_joined")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    user_id = models.ForeignKey(User, related_name="usermessages", on_delete = models.CASCADE)
    trip_id = models.ForeignKey(Trip, related_name="tripmessages", on_delete = models.CASCADE)
    messages = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    message_id = models.ForeignKey(Message, related_name="messagecomments", on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, related_name="usercomments", on_delete = models.CASCADE)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)