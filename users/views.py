from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import FormView

from config.settings import EMAIL_DEFAULT_SENDER
from users.forms import LoginForm, RegisterModelForm, SendingEmailForm
from users.authentication_form import AuthenticationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from users.models import User
from users.tokens import account_activation_token


# def login_page(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email: str = form.cleaned_data['email']
#             password: str = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('project_management')
#             else:
#                 messages.error(request, 'Invalid Username or Password')
#     else:
#         form = LoginForm()
#     return render(request, 'my_web/auth/login.html', {'form': form})


class LoginPage(LoginView):
    redirect_authenticated_user = True
    form_class = AuthenticationForm
    template_name = 'my_web/auth/login.html'

    def get_success_url(self):
        return reverse_lazy('customers')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid email or password')
        return self.render_to_response(self.get_context_data(form=form))


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                'Activate your account',
                message,
                EMAIL_DEFAULT_SENDER,
                [user.email],

            )
            email.content_subtype = 'html'
            email.send()

            return HttpResponse('<h1>Please confirm your email address to complete the registration</h1>')
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # return redirect('customers')
    else:
        form = RegisterModelForm()
    context = {'form': form}
    return render(request, 'my_web/auth/register.html', context)


class RegisterPage(FormView):
    template_name = 'my_web/auth/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
        send_mail(
            'User Succesfully Registered',
            'Test body',
            EMAIL_DEFAULT_SENDER,
            [user.email],
            fail_silently=False

        )
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


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


def active(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
