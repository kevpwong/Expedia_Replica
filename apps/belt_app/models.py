from __future__ import unicode_literals
from django.db import models
import re
from datetime import *
import bcrypt

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "Name needs at least 3 characters"
        if len(postData['username']) < 3:
            errors["username"] = "Username needs at least 3 characters"
        if len(postData['pass']) < 8:
            errors["passwordlen"] = "Password must be longer than 8 characters"
        if postData['pass'] != postData['confirm']:
            errors["passwordmatch"] = "Passwords do not match"
        return errors 
    def login_validator(self, postData):
        errors = {}
        if not User.objects.filter(username=postData['logname']):
            errors["logname"] = "Username does not exist in database"
        else:
            if not bcrypt.checkpw(postData['logpass'].encode(), User.objects.filter(username=postData['logname'])[0].password.encode()):
                errors["wrongpass"] = "Username and Password do not match"
        return errors 
    def add_validator(self, postData):
        errors = {}
        if len(postData['place']) == 0:
            errors["place"] = "Destination cannot be empty"
        if len(postData['description']) == 0:
            errors["description"] = "Description cannot be empty"
        if len(postData['start']) == 0:
            errors["start"] = "Date From cannot be empty"
        if len(postData['end']) == 0:
            errors["end"] = "Date To cannot be empty"
        if postData['start'] > postData['end']:
            errors["date"] = "Start date cannot before end date"
        return errors 


class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Place(models.Model):
    place = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start = models.DateField()
    end = models.DateField()
    users = models.ManyToManyField(User, related_name="places")
    planner = models.ForeignKey(User, related_name="planned")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)