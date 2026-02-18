from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Tweet  
from .serializers import TweetSerializer 
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username') or request.data.get('name')
    password = request.data.get('password')
    email = request.data.get('email', '')

    if not username or not password:
        return Response({'error': 'Dados incompletos'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Usuário já existe'}, status=status.HTTP_400_BAD_REQUEST)

    # Cria o usuário
    user = User.objects.create_user(username=username, password=password, email=email)
    
    # Cria o Token para esse usuário (Isso evita o erro 401 no futuro)
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'username': user.username,
        'message': 'Usuário criado com sucesso!'
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
    })

@api_view(['GET'])
@permission_classes([AllowAny]) # Mude para IsAuthenticated depois de testar
def get_feed(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    serializer = TweetSerializer(tweets, many=True)
    
    return Response({
        'results': serializer.data, 
        'next': None,
        'previous': None,
        'count': tweets.count()
    })