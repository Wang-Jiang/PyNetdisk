"""PyNetdisk URL Configuration

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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from netdisk import views as netdisk_views

urlpatterns = [
    url(r'^$', netdisk_views.index, name='netdisk_index'),
    url(r'^create_folder', netdisk_views.create_folder, name='netdisk_create_folder'),
    url(r'^edit_name', netdisk_views.edit_name, name='netdisk_edit_name'),
    url(r'^delete_file', netdisk_views.delete_file, name='netdisk_delete_file'),
    url(r'^login', netdisk_views.login, name='netdisk_login'),
    url(r'^logout', netdisk_views.logout, name='netdisk_logout'),
    url(r'^register', netdisk_views.register, name='netdisk_register'),
    url(r'^help', netdisk_views.help_page, name='netdisk_help'),
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', views.serve),
]

urlpatterns += staticfiles_urlpatterns()

