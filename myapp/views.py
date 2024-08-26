from django.shortcuts import render,redirect
from django.http import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from  .models import *
from rest_framework import status
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
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

def home (request):
    return render(request,'index.html')
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
        new_user = User(username=username, email=email, user_type=user_type)
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

        # Try to authenticate with your custom user model
        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            if user.user_type=="client" :

             return redirect("dashbord")
            else :
                return redirect("dashven")
              # Respond with "+" on successful login
        else:
            return redirect("login_view")  # Respond with "-" on failed login
    
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
        data = json.loads(request.body)
        user = User.objects.get(id=data['user_id'])  # Adjust as necessary

        print(f"user {user}")#+

        prix_total = 0

        # First, create and save the Commande object
        commande = Commande.objects.create(client=user)
        print(f"commande {commande.id}")

        # Then, add vegetables to the commande and calculate the total price
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
        
        
       
     
@login_required
@login_required
def dashboardven(request):
    section = request.GET.get('section', 'welcome')
    page_number = request.GET.get('page', 1)  # Get the page number from the request

    context = {'section': section}

    if section == 'veg':
        veg_list = Veg.objects.all()
        paginator = Paginator(veg_list, 3)  # Show 10 veg per page
        page_obj = paginator.get_page(page_number)
        context['vegs'] = page_obj
        context['paginator'] = paginator

    elif section == 'messages':
        message_list = Message.objects.all()
        paginator = Paginator(message_list, 10)  # Show 10 messages per page
        page_obj = paginator.get_page(page_number)
        context['messages'] = page_obj
        context['paginator'] = paginator

    elif section == 'users':
        user_list = User.objects.all()
        paginator = Paginator(user_list, 3)  # Show 10 users per page
        page_obj = paginator.get_page(page_number)
        context['users'] = page_obj
        context['paginator'] = paginator

    elif section == 'commandes':
        commandes_list = Commande.objects.all()
        paginator = Paginator(commandes_list, 10)  # Show 10 commandes per page
        page_obj = paginator.get_page(page_number)
        context['commandes'] = page_obj
        context['paginator'] = paginator

    return render(request, 'dashbordven.html', context)
def logout(request):
    logout(request)
    return redirect("index")


        
      
          
        
          



     
     
     
   

