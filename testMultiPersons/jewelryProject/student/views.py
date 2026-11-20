from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Student


def student(request):
    # template = loader.get_template("student.html")
    context = {
        "students": Student.objects.all(),
        "programming": "student",
    }
    # return HttpResponse(template.render())
    return render(request, "student.html", context)


def studentDetails(request):
    template = loader.get_template("details.html")
    context = {
        "students": Student.objects.all(),
        "programming": "student",
    }
    # return HttpResponse(template.render())
    return render(request, "details.html", context)


def student_detail(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    context = {
        "student": student,  # single student object
        "programming": "student",
    }

    # return HttpResponse(template.render())
    return render(request, "details.html", context)
