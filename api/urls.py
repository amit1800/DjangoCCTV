from django.urls import path
from api import views

urlpatterns = [
    path("api/auth", views.authenticate),
]
