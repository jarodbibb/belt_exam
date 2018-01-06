from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from models import *

import bcrypt

def index(request):
    return render(request, 'first_app/index.html')

def success(request):

    user = User.objects.get(id = request.session['id'])
    my_wish = List.objects.filter(users = request.session['id']).exclude(created_by = request.session['id'])
    my_create = List.objects.filter(created_by = request.session['id'])
    all_item = List.objects.all().exclude(created_by = request.session['id']).exclude(users = request.session['id'])
   
    try:
        context = {
            "user": user,
            'my_wish': my_wish,
            'all_item': all_item,
            'my_create': my_create,
           
        }
        
        return render(request, "first_app/profile.html", context)
    except:
        
        return redirect('/')

def suggest(request):
    user = User.objects.get(id = request.session['id'])
    context = {
        'user': user,
    }
    return render(request, "first_app/add_item.html", context)

def see_users(request, id):
    listed = List.objects.get(id = id)
    user = User.objects.get(id = request.session['id'])
    liker = User.objects.filter(lists = id)
    context = {
        'listed': listed,
        'user': user,
        'liker': liker,
    }

    return render(request, "first_app/see_um.html", context)


def add_item(request, id):
    List.objects.add_to_list(id, request.session['id'])
    return redirect('/success')


def login(request):
    result = User.objects.login_val(request.POST)
    if type(result) == dict:
        for error in result.itervalues():
            messages.error(request, error, extra_tags="log")
        return redirect('/')
    
    request.session['id'] = result.id

    
    return redirect('/success')

def register(request):
    errors = User.objects.register_val(request.POST)
    if errors:
        for error in errors.itervalues():
            messages.error(request, error, extra_tags="reg")
        return redirect("/")

    password = request.POST["password"]
    hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5)) 
    user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST["last_name"],email = request.POST["email"], password = hashed)
   
    request.session['id'] = user.id
    return redirect('/success')


def logout(request):
    request.session.clear()
    return redirect('/')

def create(request):
    errors = List.objects.list_val(request.POST, request.session['id'])
    context = {
        'errors': errors,
    }
    if type(errors) == list:
        for error in errors:
            messages.error(request, error)
        return redirect('suggest', context)
    return redirect('/success')

def delete(request, id):
    List.objects.delete(id, request.session['id'])
    return redirect('/success')

def remove(request, id):
    print "hello"
    List.objects.remove_item(id, request.session['id'])
    return redirect('/success')







