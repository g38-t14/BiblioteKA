from django.urls import path
from . import views

urlpatterns = [
    path("loans/<int:loan_id>/return/", views.ReturnBookView.as_view()),
]
