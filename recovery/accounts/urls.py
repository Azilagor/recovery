from django.urls import path
from .views import password_reset

urlpatterns = [
    path('reset/', password_reset, name='password_reset'),
]
