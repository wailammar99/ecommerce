from rest_framework import serializers
from .models import *

class VegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veg
        fields = '__all__'  # or specify the fields you want to include
class CommandeSerializer(serializers.ModelSerializer):
    vegs=VegSerializer(many=True)
    class Meta :
        model =Commande
        fields="__all__"