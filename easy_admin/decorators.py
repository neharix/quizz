from functools import wraps

from django.http import HttpRequest
from django.shortcuts import redirect


def staff_only(function):
    @wraps(function)
    def wrap(request: HttpRequest, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            return redirect("home")

    return wrap
