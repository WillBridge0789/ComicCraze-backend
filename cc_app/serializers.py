from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *


class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'purchaser', 'items', 'is_gift', 'gift_message')

class UserReadSerializer(serializers.ModelSerializer):
    favorite_comics = ComicSerializer(many=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'favorite_comics')

class UserWriteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    favorite_comics = serializers.PrimaryKeyRelatedField(queryset=Comic.objects.all(), many=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name', 'favorite_comics')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
