# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bcrypt
import re

from django.db import models

LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
class UserManager(models.Manager):
    def register_val(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name']= "Blog name should be more than 2 characters"
        elif not LETTER_REGEX.match(postData["first_name"]):
            errors["first_name_valid"] = "First name must be letters only"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Blog name should be more than 2 characters"
        elif not LETTER_REGEX.match(postData["last_name"]):
            errors["last_name_valid"] = "Last name must be letters only"

        if not EMAIL_REGEX.match(postData["email"]):
            errors["email_valid"] = "Email entered is invalid"
        
        if len(postData["password"]) < 8:
            errors["password"] = "Must be 8 characters long"
        elif postData["password"]!= postData["confirm_password"]:
            errors['password'] = "Passwords do not match"

        if not errors and User.objects.filter(email=postData["email"]):
            errors["email_valid"] = "Email is already registered"
      
        
        return errors
    
    def login_val(self, postData):
        errors = {}
        users = User.objects.filter(email= postData['email'])
        if not users:
            errors['login'] = "Email not found"
        else:
            user = users[0]
            if not bcrypt.checkpw(postData["password"].encode(), user.password.encode()):
                errors["login"] = "Incorrect password"
        
        if not errors:
            return user

class ListManager(models.Manager):
    def list_val(self, postData, id):
        errors = []
        if len(postData["product"]) < 4:
            errors.append('Product name should be atleast FOUR characters')

        else:
            try: 
                new_product = List.object.get(item = postData['product'])
            
            except:
                new_product = List.objects.create(
                    item = postData['product'],
                    created_by = User.objects.get(id = id)
            )
    def add_to_list(self, item_id, user):
        me = User.objects.get(id = user)
        item_add = List.objects.get(id = item_id)
        me.lists.add(item_add)
        me.save()

    def remove_item(self, item_id, user):
        me = User.objects.get(id = user)
        item_delete = List.objects.get(id = item_id)
        me.lists.remove(item_delete)
        me.save()
        return item_delete
    
    def delete(self, item_id, user):
        List.objects.get(id = item_id).delete()



        
        
        

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()
    friend = models.ManyToManyField("self")

    def __repr__(self):
        return "<User object:{} {} {} {}>".format(self.first_name, self.last_name, self.email, self.password)

class List(models.Model):
    item = models.CharField(max_length = 255)
    created_by = models.ForeignKey(User, related_name = "made")
    users = models.ManyToManyField(User, related_name = 'lists')
    created_at = models.DateTimeField(auto_now_add=True) 
    objects = ListManager()







