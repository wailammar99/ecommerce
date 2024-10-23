from django.contrib import admin
from .models import *

@admin.register(Veg)
class VegAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'existe')  # Columns to display in the list view
    search_fields = ('name',)  # Fields to search
    list_filter = ('existe',)  # Filters to apply
    ordering = ('name',)  # Default ordering

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'msg')
    search_fields = ('name', 'email')
    ordering = ('name',)

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type')
    search_fields = ('username', 'email')
    list_filter = ('user_type',)
    ordering = ('username',)
@admin.register(Commande)
class CommandeAdmin( admin.ModelAdmin ) :
    list_display=('id',"prix_total")

admin.site.register(Cat)