from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404

from users.models import UserExtension
from users.forms import UserRegistrationForm, ProfileEditForm
from users.tokens import password_token_gen

from datetime import date

from publications.models import Publication

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


class ProfileView(generic.View):
    template_name = 'user_profile.html'

    def get_context_data(self) -> dict:
        context = {}

        publications = Publication.objects.filter(author=self.request.user).order_by('pub_date')
        context['publications'] = publications

        return context


    def get_initial(self) -> dict:
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


    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = ProfileEditForm(initial=self.get_initial())
        context['form'] = form

        return render(request, self.template_name, context)
    

    def post(self, request, *args, **kwargs):
        form = ProfileEditForm(request.POST, initial=self.get_initial())
        context = self.get_context_data()

        user = request.user
        extension = user.extension

        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            day = int(form.cleaned_data['day'])
            month = int(form.cleaned_data['month'])
            year = int(form.cleaned_data['year'])

            extension.birthdate = date(year, month, day)
            extension.save()

            return redirect(reverse('users:profile'))
        else:
            print(form.errors)

        context['form'] = form

        return render(request, self.template_name, context)




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


class PasswordResetView(generic.View):
    template_name = 'user_password_reset.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

    def post(self, request, *args, **kwargs):
        error_message = ''
        sent_mail = False
        email = request.POST.get('email')

        try:
            email = str(email)
        except:
            error_message = 'Please enter a valid email!'

        if len(error_message) == 0:
            user = User.objects.filter(email=email).first()
            sent_mail = True
            if user:
                token = password_token_gen.make_token(user)
                encodeduid = urlsafe_base64_encode(force_bytes(user.pk))

                url = settings.SITE_URL + reverse('users:restablish_password') + f'?token={token}&uuid={encodeduid}'
                send_mail(
                    'Reset Password',
                    f'Follow this url to reset password \nURL: {url}',
                    from_email='flasker@flasker.com',
                    recipient_list=['test@test.com']
                )

        return render(request, self.template_name, {'error_message': error_message, 'sent_mail': sent_mail})


class RestablishPasswordView(generic.View):
    template_name = 'user_restablish_password.html'


    def get(self, request, *args, **kwargs):

        encoded_uuid = request.GET.get('uuid')
        token = request.GET.get('token')

        if not encoded_uuid or not token:
            raise Http404
        
        try:
            uuid = force_str(urlsafe_base64_decode(encoded_uuid))
            user = User.objects.filter(pk=uuid).first()
        except ValueError:
            raise Http404


        if not password_token_gen.check_token(user, token):
            raise Http404
        
        return render(request, self.template_name)


    def post(self, request, *args, **kwargs):

        encoded_uuid = request.GET.get('uuid')
        token = request.GET.get('token')
        error_message = ''


        if not encoded_uuid or not token:
            raise Http404
        
        try:
            uuid = force_str(urlsafe_base64_decode(encoded_uuid))
            user = User.objects.filter(pk=uuid).first()
        except:
            raise Http404

        if not password_token_gen.check_token(user, token):
            raise Http404
        
        unsanitized_password = request.POST.get('password')
        unsanitized_v_password = request.POST.get('v_password')

        password = str(unsanitized_password)
        v_password = str(unsanitized_v_password)

        if password == v_password:
            user.set_password(password)
            user.save()
            return redirect(reverse('users:login'))
        else:
            error_message = 'Passwords don\'t match'

        return render(request, self.template_name, {'error_message': error_message })