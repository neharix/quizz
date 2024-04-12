from django.shortcuts import render


def tools(request):
    context = {}
    return render(request, "tools.html", context)
