# from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('main', views.main),
    path('register', views.register),
    path('login', views.login),
    path('events', views.events),
    path('events/add', views.addpage),
    path('add', views.add),
    path('events/destination/<tripid>', views.destination),
    path('join/<tripid>', views.join),
    path('logout', views.logout),
    path('upload', views.upload)
    # path('admin/', admin.site.urls),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)