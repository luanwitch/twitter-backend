from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import TweetViewSet, register_user, get_user_profile, get_feed
from rest_framework.authtoken import views as auth_views

router = DefaultRouter()
# O React está tentando postar em /api/posts/, então registramos como 'posts'
router.register(r'posts', TweetViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Autenticação
    path('api/auth/login/', auth_views.obtain_auth_token),
    path('api/auth/register/', register_user),
    path('api/users/me/', get_user_profile),
    
    # O React busca o Feed neste endereço específico:
    path('api/feed/', get_feed), 
    
    # Inclui as rotas do router (isso vai criar o /api/posts/)
    path('api/', include(router.urls)),
]