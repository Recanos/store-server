from typing import Any

from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView

from common.views import titleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('index')

class UserRegistrationView(titleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_message = "Вы зарегестрировались!"
    success_url = reverse_lazy('users:login')
    title = "Регистрация"

class UserProfileView(titleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store-профиль'
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.id, ))

class EmailVerificationView(titleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Верификация'

    def get(self, request, *args, **kwargs):  
        code = kwargs['code']
        user = User.objects.get(email=kwargs.get('email'))
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.last().is_expired():
            user.is_verified = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))

