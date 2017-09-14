"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from fire import views
from fire import urls as fire_urls
from django.views.static import serve
import upload
import settings
import os

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^fire/', include(fire_urls, namespace='fire')),
    url(r'^$', views.index, name='index'),

    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload.upload_image, name='upload_image'),
    url(r"^upload/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, }),
]