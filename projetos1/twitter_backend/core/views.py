from rest_framework import viewsets, permissions
from .models import Tweet
from .serializers import TweetSerializer
from core import models

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

 # No core/views.py, dentro da classe TweetViewSet:
def get_queryset(self):
    user = self.request.user
    if user.is_authenticated:
        # Retorna tweets do próprio usuário e de quem ele segue
        following_users = user.profile.follows.all().values_list('user', flat=True)
        return Tweet.objects.filter(models.Q(user__in=following_users) | models.Q(user=user)).order_by('-created_at')
    return Tweet.objects.all().order_by('-created_at')       