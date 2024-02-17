from rest_framework import serializers
from django.contrib.auth import get_user_model
from reviews.models import Review
from movies.models import Movie
from .models import User
from django.utils.timezone import now
from movies.models import Rating

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'


# class ProfileSerializer(serializers.ModelSerializer):
#     days_since_joined = serializers.SerializerMethodField(read_only=True)

#     class Meta:
#         model = get_user_model()
#         fields = ('id', 'username', 'email', 'wishlist', 'date_joined', 'rating_set', 'days_since_joined')
    
  