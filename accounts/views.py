from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from .forms import LoginForm, RegisterForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib import messages

User = get_user_model()


def login_view(request):
    login_form = LoginForm()
    next_ = request.GET.get("next", None)
    if request.method == "POST":
        login_form = LoginForm(request.POST or None)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            if next_:
                redirect(next_)
            return redirect("blogs:blog")
    context = {
        "login_form": login_form
    }
    return render(request, "accounts/login.html", context)


def register_view(request):
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        new_user = register_form.save()
        uuid = urlsafe_base64_encode(smart_bytes(new_user.slug))
        token = PasswordResetTokenGenerator().make_token(new_user)
        link = request.build_absolute_uri(reverse_lazy("accounts:activation", kwargs={"uuid": uuid, "token": token}))
        send_mail(
            "Blogger",
            f"Linke kecid edib hesabinizi aktivlesdirin\n{link}",
            settings.EMAIL_HOST_USER,
            [new_user.email],
            fail_silently=True
        )
        return redirect("blogs:blog")
    context = {
        "register_form": register_form
    }
    return render(request, "accounts/register.html", context)


def logout_view(request):
    logout(request)
    return redirect("blogs:blog")


def activation_view_complete(request, uuid, token):
    slug = smart_str(urlsafe_base64_decode(uuid))
    user = User.objects.get(slug=slug)

    if not PasswordResetTokenGenerator().check_token(user, token):
        message = "Link duzgun deil!"
        messages.error(request, message)
        return redirect("accounts:login")
    user.is_active=True
    user.save()
    return redirect("accounts:login")





