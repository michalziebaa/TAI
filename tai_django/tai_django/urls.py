"""tai_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from tai_django.core import views
from tai_django import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.urls import path, include
# from views import log_in, log_out, register, activate
from tai_django.core.views import log_in, log_out, register, activate

urlpatterns = [
    path('', views.upload, name='upload'),
    path('login/', log_in),
    path('logout/', log_out),
    path('register/', register),
    path('activate/<uidb64>/<token>', activate, name="activate"),
    path('upload/', views.upload, name='upload'),
    path('admin/', admin.site.urls),
    path('download/', views.download, name='download'),
    # path('<str:filepath>/', views.download_file)
    # path('<str:filepath>/', views.download_file)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)