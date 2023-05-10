from django.urls import path
from books.views import BookView
from loans.views import LoanView

urlpatterns = [
    path("books/", BookView.as_view()),
    path("books/<int:id>/loans/", LoanView.as_view()),
]
