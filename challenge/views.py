import random

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from challenge.models import *

from .utils import *


def logout_view(request: HttpRequest):
    logout(request)
    return redirect("home")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        if request.POST.get("first_name", False) and request.POST.get(
            "last_name", False
        ):
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            username = remove_turkmen_letter(last_name.lower() + first_name.lower())

            if contains_cyrillic(username):
                username = transliterate(username)

            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    email="stub@mail.tm",
                    password=username + str(random.randint(1000000, 9999999)),
                    last_name=last_name,
                    first_name=first_name,
                )
                if request.POST.get("agency", False):
                    profile = Profile.objects.get(user=user)
                    profile.about = request.POST.get("agency")
                    profile.save()

            login(request, user)
            print(user.username)
            return redirect("home")

    context = {}
    return render(request, "views/login.html", context)


def index(request: HttpRequest):
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect("easy_tools")
        else:
            return redirect("/superuser/login/")
    return redirect("/superuser/login/")
