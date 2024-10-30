from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.timezone import now



class Catlogue(models.Model):
    nom=models.CharField( max_length=50)
    def __str__(self) :
        return f"{self.nom}"
    

#+
class Catlogue(models.Model):#+
    nom=models.CharField( max_length=50)#+
class Veg(models.Model):
#-
    catalogue=models.ForeignKey(Catlogue,on_delete=models.CASCADE,null=True,blank=True)#-
   
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to="veg", null=True, blank=True)
    existe = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=200)
    msg = models.CharField(max_length=200)

    def __str__(self):
        return self.email

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
        ('vendeuse', 'Vendeuse'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return self.username

class Commande(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commandes")
    vegs = models.ManyToManyField(Veg, related_name="commandes")
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    Etat_choice = (
        ('annule', 'Annule'),
        ('En cour ', 'en cour '),
        ('livre', 'livre'),
        ('Nouveux', 'nouveux')
    )
    etat = models.CharField(max_length=10, choices=Etat_choice,default="nouveux")
