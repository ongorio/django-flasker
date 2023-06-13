from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import transaction

from django.contrib.auth.models import User
from users.models import UserExtension
from users.forms import UserRegistrationForm, ProfileEditForm

from datetime import date


class RegisterView(generic.View):
    template_name = 'user_registration.html'
    form_class = UserRegistrationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        error_message = None

        if form.is_valid():

            try:
                with transaction.atomic():
                    user = User()
                    extension = UserExtension()

                    user.username = form.cleaned_data['username']
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.email = form.cleaned_data['email']
                    user.set_password(form.cleaned_data['password'])

                    user.save()

                    day = int(form.cleaned_data['day'])
                    month = int(form.cleaned_data['month'])
                    year = int(form.cleaned_data['year'])

                    extension.birthdate = date(year, month, day)
                    extension.user = user

                    extension.save()

                    return redirect(reverse('users:login'))
            except:
                error_message = 'Something wen\'t wrong!'
        else:
            print(form.errors)

        return render(request, self.template_name, context={'form': form, 'error_message': error_message})


class ProfileView(generic.TemplateView):
    template_name = 'user_profile.html'


class ProfileEditView(generic.FormView):
    template_name = 'user_profile_edit.html'
    form_class = ProfileEditForm

    def get_initial(self):
        initial = {}
        user = self.request.user
        extension = user.extension

        initial['username'] = user.username
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email

        initial['day'] = extension.birthdate.day
        initial['month'] =extension.birthdate.month
        initial['year'] = extension.birthdate.year
         

        return initial



    def form_valid(self, form: ProfileEditForm):
        
        user = self.request.user
        extension = user.extension

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()

        day = int(form.cleaned_data['day'])
        month = int(form.cleaned_data['month'])
        year = int(form.cleaned_data['year'])


        extension.birthdate = date(year, month, day)
        extension.save()


        return redirect(reverse('users:profile'))



class LoginView(generic.View):
    template_name = 'login.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        error_message = ''

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse('users:profile'))
        else:
            error_message = 'Username/Password aren\'t correct!'

        return render(request, self.template_name, {'error_message': error_message})


class LogoutView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect(reverse('index'))
