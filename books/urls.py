from django.urls import path
from . import views
from loans.views import LoanView

urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<int:id>/loans/", LoanView.as_view()),
]
