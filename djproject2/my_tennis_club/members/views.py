# from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import loader


# def members(request):
#     template = loader.get_template("myfirst.html")
#     context = {"programming": "python"}
#     # return HttpResponse(template.render())
#     return render(request, "myfirst.html", context)

from django.http import HttpResponse
from django.template import loader
from .models import Member

def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))
