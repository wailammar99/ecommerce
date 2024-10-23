from django.shortcuts import render,redirect
from .forms import VegForm
from django.http import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from  .models import *
from rest_framework import status
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import *
from django.contrib.auth.models import User 
from django.contrib import messages
from django.db import models

from django.contrib.auth.hashers import make_password
from  .serializers   import *
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from django.views import View
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


User = get_user_model()





# Create your views here.
oui =False


def index(request):
    vegs=Veg.objects.all()
    
    return render(request, 'index.html', {'vegs': vegs})

def home(request):
    role = None  # Default value for unauthenticated users
    if request.user.is_authenticated:
        role = request.user.user_type 
        print(f"role is {role }")
    
    return render(request, 'index.html', {"role": role})
def shop (request):
    vegs=Veg.objects.all()
    return render(request,"shop.html",{"vegs":vegs})
def dashbord (request):
    return render (request,"dashbord.html")
def contact (request):
      messagee=None
      if request.method == 'POST':
        nam = request.POST['name']
        phon = request.POST['phone']
        emai = request.POST['email']
        m = request.POST['m']
        new_message = Message(name=nam, phone=phon,email=emai, msg=m)
        new_message.save()
        if new_message.id :
            messagee="le message est bien envoye "
        else :
            messagee="echech de enviyer le message "

      return render(request,"contact.html",{"messagee": messagee})
def blog (request):
    return render(request,"blog.html")

def about (request):
    return render(request,"about.html")
def register (request):
    return render(request,"regg.html")

def vegg (request):
     vegs=Veg.objects.all()
     return render(request,"vagetables.html",{"vegs":vegs})
def test2 (request ):
          
          
          return render(request,"test2.html")


def reg(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        user_type = request.POST.get('category', None)  # Use 'category' as per the form field name

        if password1 != password2:
            messages.error(request, 'The passwords do not match')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        # Create new user instance
        new_user = User(username=username, email=email, user_type=user_type,is_staff=False)
        new_user.set_password(password1)
        new_user.save()

        messages.success(request, "You have been registered successfully")
        return redirect("login_view")
        

def registemessage(request):
  
    if request.method == 'POST':
        message=message()
        nam = request.POST.GET['name']
        phon = request.POST.GET['phone']
        emai = request.POST.get['email']
        m = request.POST.get['m']
        message.name=nam 
        message.phone=phon
        message.email=emai
        message.msg=m 
        message.save()
        


# views.py
class ClientAuthBackend(ModelBackend):
   pass

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect based on user_type
            if user.user_type == "client":
                return redirect("dashbord")
            elif user.user_type == "vendeuse":
                return redirect("dashven")
            elif user.user_type == "admin":
                return redirect("/admin/")
        else:
            # Add an error message when authentication fails
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login_view')
    
    return render(request, 'conx.html')


def veg_details(request, veg_id):
    if request.method == "GET":
        try:
            veg_instance = Veg.objects.get(id=veg_id)  # Fetch a single instance
            ser = VegSerializer(veg_instance)  # Do not use many=True for a single instance
            return JsonResponse(ser.data, safe=False)
        except Veg.DoesNotExist:
            return JsonResponse({"error": "Vegetable not found"}, status=404)







def commande_view(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            print("User is not authenticated")
            return redirect("login")
        
        # Load data from the request body
        data = json.loads(request.body)
        
        # Get the user by ID
        user = User.objects.get(id=data['user_id'])
        print(f"user {user}")
        
        prix_total = 0

        # Create and save the Commande object
        commande = Commande.objects.create(client=user)
        print(f"commande {commande.id}")

        # Add vegetables to the commande and calculate total price
        for veg_id in data['vegs']:
            veg_instance = Veg.objects.get(id=veg_id)
            prix_total += veg_instance.price
            commande.vegs.add(veg_instance)
        
        # Update the prix_total field and save the commande again
        commande.prix_total = prix_total
        commande.save()

        return JsonResponse({'message': 'Commande created successfully'}, status=201)
    
    elif request.method == "GET":
        commandes = Commande.objects.all().values()
        return JsonResponse(list(commandes), safe=False, status=200)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
        
def commande_detail(request, commande_id):
    if request.method == "GET":
        try:
            commande_cible = Commande.objects.get(id=commande_id)
            serializer = CommandeSerializer(commande_cible)  # Removed many=True
            return JsonResponse(serializer.data, status=200)
        except Commande.DoesNotExist:
            return JsonResponse({"error": "La commande est introuvable"}, status=404)
          
@login_required
def dashboardven(request):
    section = request.GET.get('section', 'veg')  # Default to 'veg' if no section is specified
    vegs, messages, users, commandes = [], [], [], []
    form = None  # Initialize form as None to avoid UnboundLocalError

    # Pagination setup
    veg_page_number = request.GET.get('page', 1)
    messages_page_number = request.GET.get('page', 1)
    users_page_number = request.GET.get('page', 1)
    commandes_page_number = request.GET.get('page', 1)

    if section == 'veg':
        if request.method == 'POST':
            form = VegForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('dashboardven')  # Redirect to avoid re-submitting the form on refresh
        else:
            form = VegForm()
        vegs = Veg.objects.all()
        veg_paginator = Paginator(vegs, 5)  # Show 10 vegs per page
        vegs = veg_paginator.get_page(veg_page_number)

    elif section == 'messages':
        messages = Message.objects.all()
        messages_paginator = Paginator(messages, 10)  # Show 10 messages per page
        messages = messages_paginator.get_page(messages_page_number)

    elif section == 'users':
        users = User.objects.all()
        users_paginator = Paginator(users, 5)  # Show 10 users per page
        users = users_paginator.get_page(users_page_number)

    elif section == 'commandes':
        commandes = Commande.objects.all()
        commandes_paginator = Paginator(commandes, 10)  # Show 10 commandes per page
        commandes = commandes_paginator.get_page(commandes_page_number)

    context = {
    'section': section,
    'vegs': vegs,
    'messages': messages,
    'users': users,
    'commandes': commandes,
    'veg_paginator': veg_paginator if section == 'veg' else None,
    'messages_paginator': messages_paginator if section == 'messages' else None,
    'users_paginator': users_paginator if section == 'users' else None,
    'commandes_paginator': commandes_paginator if section == 'commandes' else None,
    'form': form,
}
    return render(request, 'dashbordven.html', context)

@csrf_exempt
def logout_view(request):
    logout(request)
    print("Logout successful")
    return redirect("login_view")

#crud veg 
@login_required 
def delete_veg(request,id_veg):
    if request.method=="DELETE" :
        try :
            veg=Veg.objects.get(id=id_veg)
            veg.delete()
            return JsonResponse({"message":"the prodcest has benn delete "},status=200)
        except Veg.DoesNotExist :
            return JsonResponse({"message":"the prodcest not fund  "},status=404)
    else :
        return JsonResponse({"eroor":"methode not allow "},status=405)
@login_required
def create_veg_view(request):
    if request.method == 'POST':
        form = VegForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Replace with your success URL
    else:
        form = VegForm()

    return render(request, 'create_veg.html', {'form': form})

          
        
          



     
     
     
   
