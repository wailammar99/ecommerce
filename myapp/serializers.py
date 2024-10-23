from rest_framework import serializers
from .models import Veg, Message, User, Commande

class VegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veg
        fields = '__all__'  # Serialize all fields of Veg

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'  # Serialize all fields of Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Serialize all fields of User

class CommandeSerializer(serializers.ModelSerializer):
    client = UserSerializer()  # Use UserSerializer to serialize the client field
    vegs = VegSerializer(many=True)  # Nested serialization for ManyToManyField

    class Meta:
        model = Commande
        fields = '__all__'  # Serialize all fields of Commande
