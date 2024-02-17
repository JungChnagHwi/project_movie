from django.urls import path
from accounts import views

urlpatterns = [
  path('user/', views.profile),
]
