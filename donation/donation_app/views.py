from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Institution, Donation
from django.core.paginator import Paginator
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout


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

        institutions = Institution.objects.all()
        foundations_list = []
        corporates_list = []
        individuals_list = []
        for institution in institutions:
            categories = Category.objects.filter(institution__id=institution.id)
            categories_names = ', '.join([category.name for category in categories])
            if institution.type == 0:
                foundations_list.append((institution, categories_names))
            elif institution.type == 1:
                corporates_list.append((institution, categories_names))
            elif institution.type == 2:
                individuals_list.append((institution, categories_names))

        foundation_paginator = Paginator(foundations_list, 1)
        corporate_paginator = Paginator(corporates_list, 1)
        individual_paginator = Paginator(individuals_list, 1)

        page = request.GET.get('page')
        foundations = foundation_paginator.get_page(page)
        corporates = corporate_paginator.get_page(page)
        individuals = individual_paginator.get_page(page)

        ctx = {'amount_of_institutions': amount_of_institutions,
               'quantity_of_donations': quantity_of_donations,
               'foundations': foundations,
               'corporates': corporates,
               'individuals': individuals
               }
        return render(request, 'index.html', ctx)


class Register(View):
    def get(self, request):
        form = RegisterForm()
        ctx = {'form': form}
        return render(request, 'register.html', ctx)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = email
            password = form.cleaned_data['password']
            password_confirmation = form.cleaned_data['password_confirmation']
            if password == password_confirmation:
                user = User.objects.create_user(username=username,
                                                first_name=first_name,
                                                last_name=last_name,
                                                email=email,
                                                password=password)
                return redirect('login')
            else:
                return HttpResponse("Invalid data")
        return HttpResponse("Invalid data")


class Login(View):
    def get(self, request):
        form = LoginForm()
        ctx = {'form': form}
        return render(request, 'login.html', ctx)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('landing_page')
            else:
                return redirect('register')


class AddDonation(View):
    def get(self, request):
        if request.user.is_authenticated:
            ctx = {'data': "sampledata",
                   'logged_user': request.user}
        else:
            ctx = {'data': "sampledata"}
        return render(request, 'form.html', ctx)


class Logout(View):
    def get(self, request):
        if request.user:
            logout(request)
        return redirect('landing_page')




