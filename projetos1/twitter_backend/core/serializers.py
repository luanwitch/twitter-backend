from rest_framework import serializers
from .models import Tweet
from django.contrib.auth.models import User

class TweetSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Tweet
        fields = ['id', 'username', 'content', 'created_at', 'likes']