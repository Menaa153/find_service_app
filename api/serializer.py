from rest_framework import serializers
from .models import Producto
from django.contrib.auth import get_user_model

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'role', 'categoria', 'descripcion', 'location']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'role', 'first_name', 'last_name', 'phone')

    def validate_email(self, value):
        """ Verifica que el email no esté en uso """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("El email ya está registrado.")
        return value

    def validate_username(self, value):
        """ Verifica que el username no esté en uso """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")
        return value

    def create(self, validated_data):
        """ Crea el usuario con los datos validados """
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            role=validated_data.get('role', User.CLIENTE),  # Cliente por defecto
            first_name=validated_data.get('first_name', ''),  
            last_name=validated_data.get('last_name', ''),  
            phone=validated_data.get('phone', None)  
        )
        user.set_password(validated_data['password'])  #  Encriptar la contraseña
        user.save()
        return user
