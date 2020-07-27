"""mainproject URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from firstWEB import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',views.index),
    url(r'^templefile/',views.templefile),
    url(r'^cal/',views.cal),
    url(r'^caltwonumber/',views.caltwonumber),
    url(r'^cisco/',views.cisco),
    url(r'^save_xml/',views.save_xml),
    url(r'^add_interface/',views.add_interface),
    url(r'^load_deletp_page/',views.load_deletp_page),
    url(r'^get_interface_name/',views.get_interface_name,name='check'),
    url(r'^show_all_interface/',views.show_all_interface),
    url(r'^add_interFaceFromTable/',views.add_interFaceFromTable),
    url(r'^add_inter_with_form/',views.add_inter_with_form,name='addinterface'),
    url(r'^parsexml/',views.parsexml),
    url(r'^edit_show/',views.edit_show),
    url(r'^delete_show/',views.delete_show),
    url(r'^edit_inter_with_form/',views.edit_inter_with_form,name='editinterface'),


]
