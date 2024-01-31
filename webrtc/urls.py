"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import MainView, views, p2pHttpViews, p2pSocket, p2sSocket

urlpatterns = [
    path("p2sOffer", MainView.p2sOffer),
    path("s2sOffer", MainView.s2sOffer),
    path("p2sHttp", MainView.p2sHttpIndex),

    path("", MainView.p2sHttpIndex),
    path("getOffer", p2pHttpViews.getOffer),
    path("getAnswer", p2pHttpViews.getAnswer),
    path("p2pHttp", p2pHttpViews.p2pHttpIndex),
    path("setOffer", p2pHttpViews.setOffer),
    path("setAnswer", p2pHttpViews.setAnswer),
    path("p2pSocket", p2pSocket.p2pSocketIndex),
    path("p2sSocket", p2sSocket.p2sSocketIndex),
]
