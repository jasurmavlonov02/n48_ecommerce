from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import View

from config.settings import EMAIL_DEFAULT_SENDER
from users.forms import LoginForm, RegisterModelForm, SendingEmailForm


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email: str = form.cleaned_data['email']
            password: str = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('project_management')
            else:
                messages.error(request, 'Invalid Username or Password')
    else:
        form = LoginForm()
    return render(request, 'my_web/auth/login.html', {'form': form})


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            send_mail(
                'User Succesfully Registered',
                'Test body',
                EMAIL_DEFAULT_SENDER,
                [user.email],
                fail_silently=False

            )
            login(request, user)
            return redirect('customers')
    else:
        form = RegisterModelForm()
    context = {'form': form}
    return render(request, 'my_web/auth/register.html', context)


# FormView

def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('customers')


class SendingEmail(View):
    sent = False

    def get(self, request, *args, **kwargs):
        form = SendingEmailForm()
        context = {
            'form': form,
            'sent': self.sent
        }
        return render(request, 'users/send-email.html', context)

    def post(self, request, *args, **kwargs):
        form = SendingEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            recipient_list = form.cleaned_data['recipient_list']
            send_mail(
                subject,
                message,
                EMAIL_DEFAULT_SENDER,
                recipient_list,
                fail_silently=False
            )
            self.sent = True
            context = {
                'form': form,
                'sent': self.sent
            }
            return render(request, 'users/send-email.html', context)
