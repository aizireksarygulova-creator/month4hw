from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Profile
from django.contrib.auth.decorators import login_required

from .forms import RegisterForms, LoginForms, UpdateProfileForm

# Create your views here.

# Аунтентификация - поиск пользователя в бд
# Авторизация - проверка прав доступа пользователя 
# Регистрация - создание нового пользователя


def register(request):
    if request.method == "GET":
        forms = RegisterForms()
        return render(request, "users/register.html", context={"forms": forms})
    if request.method == "POST":
        forms = RegisterForms(request.POST)
        if not forms.is_valid():
            return HttpResponse("Error")
        user = User.objects.create_user(
            username=forms.cleaned_data.get("username"),  # pyright: ignore[reportArgumentType]
            password=forms.cleaned_data.get("password"),
        )
        Profile.objects.create(user=user)
    return redirect("/movies/")


def login_user(request):
    if request.method == "GET":
        forms = LoginForms()
        return render(request, "users/login.html", context={"forms": forms})

    if request.method == "POST":
        forms = LoginForms(request.POST)
        if not forms.is_valid():
            return HttpResponse("Error")
        user = authenticate(
            request,
            username=forms.cleaned_data.get("username"),
            password=forms.cleaned_data.get("password"),
        )

        if user is None:
            return HttpResponse("Неверный логин или пароль")

        login(request, user)
        return redirect("/movies/")


def logout_user(request):
    logout(request)
    return redirect("/")

@login_required(login_url="/login/")
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(
        request,
        "users/profile.html",
        {"profile": profile}
    )
def update_profile(request):
    if request.method == "GET":
        forms = UpdateProfileForm()
        return render(request, "users/update_profile.html", {"forms": forms})

    if request.method == "POST":
        forms = UpdateProfileForm(request.POST, request.FILES)

        if not forms.is_valid():
            return HttpResponse("Error")
        
        request.user.profile.age = forms.cleaned_data.get("age")
        request.user.profile.image = forms.cleaned_data.get("image")

        request.user.username = forms.cleaned_data.get("username")
        request.user.email = forms.cleaned_data.get("email")
        request.user.first_name = forms.cleaned_data.get("first_name")
        request.user.last_name = forms.cleaned_data.get("last_name")

        request.user.save()
        request.user.profile.save()

    return redirect("/profile/")