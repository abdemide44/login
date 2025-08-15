from django.contrib import admin
from . import views
from django.urls import include, path

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/',views.login_views,name='login'),
    path('logout/',views.logout_views,name='logout'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    path('codepassword/',views.codepassword,name='codepassword'),
    path('changepassword/',views.changepassword,name='changepassword')
    

]