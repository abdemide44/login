from django.contrib import admin
from . import views
from django.urls import  path

urlpatterns = [
path('form1/',views.form1,name='form1')
]