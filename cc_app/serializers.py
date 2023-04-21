from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser
from .models import Comic
from .models import FavoritesList


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(min_length=8, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = '__all__'


class FavoritesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritesList
        fields = '__all__'
