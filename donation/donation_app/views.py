from django.shortcuts import render, redirect
from django.views import View

# Create your views here.


class LandingPage(View):
    def get(self, request):
        ctx = {'data': "sampledata"}
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
