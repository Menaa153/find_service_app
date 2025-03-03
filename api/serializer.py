from rest_framework import serializers
from .models import Producto
from django.contrib.auth import get_user_model
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import CustomUser 

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

User = get_user_model()


class UserSerializer(GeoFeatureModelSerializer):  # Usamos GeoFeatureModelSerializer para campos geográficos
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'role', 'categoria', 'descripcion', 'location', 'profile_picture']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if instance.location:
            # Serializamos el campo `location` a un formato adecuado como un diccionario con lat y lon
            representation['location'] = {
                'latitude': instance.location.y,  # Latitud: usas 'y' si estás usando un `PointField`
                'longitude': instance.location.x,  # Longitud: usas 'x'
            }
        return representation


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


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, attrs):
        # Validación de la contraseña actual
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("La contraseña actual es incorrecta.")
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
