# from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('main', views.main),
    path('register', views.register),
    path('login', views.login),
    path('travels', views.travels),
    path('travels/add', views.addpage),
    path('add', views.add),
    path('travels/destination/<tripid>', views.destination),
    path('join/<tripid>', views.join),
    path('logout', views.logout)
    # path('admin/', admin.site.urls),
]
