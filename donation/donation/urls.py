"""
URL configuration for donation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from donation_app.views import LandingPage, AddDonation, Login, Register
from donation_app.views import Logout
from donation_app.views import TestView
from donation_app.views import UserDetails
from donation_app.views import ChangeDonationStatus
from donation_app.views import ChangeUserDetails
from donation_app.views import ChangeUserPassword
from donation_app.views import FormConfirmation


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing_page'),
    path('add_donation/', AddDonation.as_view(), name='add_donation'),
    path('form_confirmation/', FormConfirmation.as_view(), name='form_confirmation'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('testview/', TestView.as_view(), name='testview'),
    path('userdetails/', UserDetails.as_view(), name='userdetails'),
    path('changeuserdetails/<int:user_id>/', ChangeUserDetails.as_view(), name='change_user_details'),
    path('changestatus/<int:donation_id>/', ChangeDonationStatus.as_view(), name='changestatus'),
    path('changeuserpassword/<int:user_id>/', ChangeUserPassword.as_view(), name='change_user_password'),


]
