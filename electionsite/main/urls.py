from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("question1/", views.question1, name="question 1"),
    path("question1/<int:id>", views.question1_info, name="question 1 info page"),
    path("question2/", views.question2, name="question 2 "),
    path("question2/<int:id>", views.question2_info, name="question 2 info page"),
    path("question3/", views.question3, name="question 3 "),
    path("question3/<int:id>/success", views.question3_success, name="question 3 success page"),
]
