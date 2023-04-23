from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Institution, Donation
from django.core.paginator import Paginator
from .forms import RegisterForm, LoginForm, AprovingForm, APROVING_CHOICES
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


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
               'individuals': individuals,
               'logged_user': request.user,
               'is_superuser': request.user.is_superuser}
        return render(request, 'index.html', ctx)


class Register(View):
    def get(self, request):
        form = RegisterForm()
        ctx = {'form': form,
               'logged_user': request.user,
               'is_superuser': request.user.is_superuser
               }
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
        ctx = {'form': form,
               'logged_user': request.user,
               'is_superuser': request.user.is_superuser
               }
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


class AddDonation(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all()
        institutions = Institution.objects.all()
        ctx = {'categories': categories,
               'institutions': institutions,
               'logged_user': request.user,
               'is_superuser': request.user.is_superuser
               }
        return render(request, 'form.html', ctx)


class Logout(View):
    def get(self, request):
        if request.user:
            logout(request)
        return redirect('landing_page')


class UserDetails(LoginRequiredMixin, View):
    def get(self, request):
        donations = Donation.objects.filter(user_id=request.user.id).order_by('is_taken')
        donations_list = []
        for donation in donations:
            categories_list = Category.objects.filter(donation__id=donation.id)
            donations_list.append((donation.quantity,
                                   donation.institution,
                                   donation.pick_up_date,
                                   categories_list,
                                   donation.is_taken,
                                   donation.id))
        ctx = {'donations_list': donations_list,
               'categories_list': categories_list,
               'logged_user': request.user,
               'is_superuser': request.user.is_superuser}
        return render(request, 'userdetails.html', ctx)


class TestView(View):
    def get(self, request):
        # wyciągnięcie wszystkich instytucji zawierających kategorię id=1
        institutions = Institution.objects.filter(categories__id=1)

        ctx = {'institutions': institutions,
               'logged_user': request.user,
               'is_superuser': request.user.is_superuser
               }
        return render(request, 'test.html', ctx)


class ChangeDonationStatus(LoginRequiredMixin, View):

    def get(self, request, donation_id):
        form = AprovingForm()
        ctx = {'form': form,
               'logged_user': request.user}
        return render(request, 'change_status.html', ctx)

    def post(self, request, donation_id):
        form = AprovingForm(request.POST)
        if form.is_valid():
            choice_dict = dict(APROVING_CHOICES)
            choice = choice_dict[int(form.cleaned_data['choice'])]
            if choice == 'tak':
                d = Donation.objects.get(id=donation_id)
                if d.is_taken:
                    d.is_taken = False
                else:
                    d.is_taken = True
                d.save()
            return redirect('userdetails')
        else:
            HttpResponse('Coś poszło nie tak')


# class AddDonation(LoginRequiredMixin, View):
#     def get(self, request):
#         if request.user.is_authenticated:
#             ctx = {'logged_user': request.user,
#                    'data': "sampledata"}
#         else:
#             ctx = {'data': "sampledata"}
#         return render(request, 'form.html', ctx)


