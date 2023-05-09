from django.urls import path
from loans.views import (
    LoanDetailView,
    LoanListDetailView,
    LoanListView,
    ReturnBookView,
)

urlpatterns = [
    path("loans/<int:loan_id>/return/", ReturnBookView.as_view()),
    path("users/loans/", LoanDetailView.as_view()),
    path("loans/all/", LoanListView.as_view()),
    path("users/<int:pk>/loans/", LoanListDetailView.as_view()),
]
