from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Institution, Donation


# Create your views here.


class LandingPage(View):
    def get(self, request):
        donations = Donation.objects.all()
        list_of_institutions = []
        quantity_of_donations = 0
        for donation in donations:
            quantity_of_donations += donation.quantity
            if donation.institution not in list_of_institutions:
                list_of_institutions.append(donation.institution)
        amount_of_institutions = len(list_of_institutions)
        ctx = {'amount_of_institutions': amount_of_institutions,
               'quantity_of_donations': quantity_of_donations}
        return render(request, 'index.html', ctx)


class AddDonation(View):
    def get(self, request):
        ctx = {'data': "sampledata"}
        return render(request, 'form.html', ctx)


class Login(View):
    def get(self, request):
        ctx = {'data': "sampledata"}
        return render(request, 'login.html', ctx)


class Register(View):
    def get(self, request):
        ctx = {'data': "sampledata"}
        return render(request, 'register.html', ctx)
