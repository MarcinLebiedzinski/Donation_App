from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Institution, Donation
from django.core.paginator import Paginator
from .forms import RegisterForm, LoginForm, AprovingForm, APROVING_CHOICES
from .forms import ChangeUserDetailsForm, ChangeUserPasswordForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

import json

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
        institutions_data_list = []
        for institution in institutions:
            category_numbers_list = []
            category_names_list = []
            for category in Category.objects.filter(institution__id=institution.id):
                category_numbers_list.append(category.id)
                category_names_list.append(category.name)
            institution_dict = {'id': institution.id,
                                'description': institution.description,
                                'name': institution.name,
                                'category_numbers': category_numbers_list,
                                'category_names': category_names_list
                                }
            institutions_data_list.append(institution_dict)

        ctx = {'categories': categories,
               'institutions_data_list': institutions_data_list,
               'logged_user': request.user,
               'is_superuser': request.user.is_superuser
               }
        return render(request, 'form.html', ctx)

    def post(self, request):
        quantity = request.POST.get("bags")
        address = request.POST.get("address")
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        institution_id = request.POST.get("organization")
        user_id = request.user.id
        is_taken = False
        categories = request.POST.getlist('categories')
        donation = Donation.objects.create(quantity=quantity,
                                           address=address,
                                           phone_number=phone_number,
                                           city=city,
                                           zip_code=zip_code,
                                           pick_up_date=pick_up_date,
                                           pick_up_time=pick_up_time,
                                           pick_up_comment=pick_up_comment,
                                           institution_id=institution_id,
                                           user_id=user_id)
        for category in categories:
            cat = Category.objects.get(id=category)
            donation.categories.add(cat)
            donation.save()

        ctx = {'quantity': quantity,
               'address': address,
               'phone_number': phone_number,
               'city': city,
               'zip_code': zip_code,
               'pick_up_date': pick_up_date,
               'pick_up_time': pick_up_time,
               'pick_up_comment': pick_up_comment,
               'institution_id': institution_id,
               'user_id': user_id,
               'is_taken': is_taken,
               'categories': categories,
               'logged_user': request.user,
               }
        return render(request, 'form-confirmation.html', ctx)


class Logout(View):
    def get(self, request):
        if request.user:
            logout(request)
        return redirect('landing_page')


class UserDetails(LoginRequiredMixin, View):
    def get(self, request):
        donations = Donation.objects.filter(user_id=request.user.id).order_by('is_taken')
        donations_list = []
        if donations:
            for donation in donations:
                categories_list = Category.objects.filter(donation__id=donation.id)
                donations_list.append((donation.quantity,
                                       donation.institution,
                                       donation.pick_up_date,
                                       categories_list,
                                       donation.is_taken,
                                       donation.id))
        else:
            categories_list = []

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


class ChangeUserDetails(LoginRequiredMixin, View):
    def get(self, request, user_id):
        form = ChangeUserDetailsForm()
        ctx = {'form': form,
               'logged_user': request.user}
        return render(request, 'change_user_details.html', ctx)

    def post(self, request, user_id):
        form = ChangeUserDetailsForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = User.objects.get(id=user_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            return redirect('userdetails')
        else:
            HttpResponse('Coś poszło nie tak')


class ChangeUserPassword(LoginRequiredMixin, View):
    def get(self, request, user_id):
        form = ChangeUserPasswordForm()
        ctx = {'form': form,
               'logged_user': request.user}
        return render(request, 'change_user_password.html', ctx)

    def post(self, request, user_id):
        form = ChangeUserPasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']
            password_confirmation = form.cleaned_data['password_confirmation']
            user = User.objects.get(id=user_id)
            if new_password == password_confirmation:
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    return redirect('userdetails')
                else:
                    return HttpResponse('Podano nieprawidłowe hasło')
            else:
                return HttpResponse('Podane hasła nie mogą się różnić')
        else:
            return HttpResponse('Coś poszło nie tak')


class FormConfirmation(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'form-confirmation.html')

