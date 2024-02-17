from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import User
from .models import Review, Comment


User = get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'like_users',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('article', 'comment_user', 'username', )