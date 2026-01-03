from django.contrib import admin
from .models import Tweet, Profile

# Registra os modelos para aparecerem no painel
admin.site.register(Tweet)
admin.site.register(Profile)