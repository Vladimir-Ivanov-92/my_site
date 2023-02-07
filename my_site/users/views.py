from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from baskets.views import basket_auth
from users.forms import UserRegistrationForm
from users.models import EmailVerification, User


class UserRegistrationAjaxView(View):

    def post(self, request):
        form = UserRegistrationForm(data=request.POST)
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse(
                data={'error': "Пользователь с указанным адресом эл. почты уже существует!"},
                status=400
            )
        elif form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                basket_auth(request)
                return JsonResponse(data={}, status=200)
            return JsonResponse(
                data={'error': form.errors.get(i) for i in form.errors},
                status=400
            )
        else:
            return JsonResponse(
                data={'error': form.errors.get(i) for i in form.errors},
                status=400
            )


class loginAjaxView(View):

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                basket_auth(request)
                return JsonResponse(data={}, status=201)
            return JsonResponse(
                data={"error": "Логин или пароль введены неверно!"},
                status=400
            )
        return JsonResponse(
            data={"error": "Введите логин и пароль"},
            status=400
        )


def LogoutUser(request):
    logout(request)
    return redirect('products_home')


def ProfileUser(request):
    return HttpResponse("ProfileUser")


class EmailVerificationView(TemplateView):
    context = {
        "title": "Подтверждение электронной почты "
    }
    template_name = 'users/email_is_verificate.html'

    def get(self, request, *args, **kwargs):
        email_code = kwargs['email_code']
        user = User.objects.get(email=kwargs['email'])
        email_verification = EmailVerification.objects.filter(user=user, email_code=email_code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            email_verification.delete()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('products_home'))
