from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def home(request):
    template = loader.get_template("myfirst.html")
    context = {"programming": "python"}
    # return HttpResponse(template.render())
    return render(request, "myfirst.html", context)
