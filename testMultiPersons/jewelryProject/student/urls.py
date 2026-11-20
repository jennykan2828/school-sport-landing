from django.urls import path
from . import views

urlpatterns = [
    path("", views.student, name="student"),
    path("details/", views.studentDetails, name="studentdetails"),
    path("details/<str:student_id>/", views.student_detail, name="student_detail"),
]
