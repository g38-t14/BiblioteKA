from rest_framework import generics

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import NotFound, PermissionDenied

from django.shortcuts import get_object_or_404

from django.utils import timezone
from datetime import timedelta

from copies.models import Copy
from books.models import Book

from .permissions import IsLoanOwner
from loans.serializers import LoanSerializer, ReturnLoanSerializer
from loans.models import Loan

from following.tasks import notify_followers


class LoanView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_blocked:
            raise PermissionDenied("You have books pending to return!")

        book_id = self.kwargs["id"]
        if not Book.objects.filter(id=book_id).exists():
            raise NotFound("Sorry! We don't have this book!")

        book_obj = get_object_or_404(Book, pk=book_id)
        copy_obj = Copy.objects.filter(book=book_obj, available=True).first()

        if copy_obj:
            duration = book_obj.max_loan_time
            return_date = timezone.now() + timedelta(days=duration)

            if return_date.weekday() == 5:
                return_date += timedelta(days=2)

            if return_date.weekday() == 6:
                return_date += timedelta(days=1)

            copy_obj.available = False
            copy_obj.save()

            serializer.save(
                loaner=user,
                return_date=return_date,
                copy=copy_obj,
            )

        else:
            raise NotFound("We no longer have samples of this book!")


class ReturnBookView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsLoanOwner]

    queryset = Loan.objects.all()
    serializer_class = ReturnLoanSerializer

    lookup_url_kwarg = "loan_id"

    def perform_update(self, serializer):
        loan_id = self.kwargs["loan_id"]
        loan = get_object_or_404(Loan, pk=loan_id)

        if loan.returned:
            raise PermissionDenied("Book already returned!")
        serializer.validated_data["returned"] = True
        serializer.save()

        copy = loan.copy
        copy.available = True
        copy.save()

        book_id = loan.copy.book.id
        notify_followers(book_id)


class LoanDetailView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        user = self.request.user

        return Loan.objects.filter(loaner=user)


class LoanListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanListDetailView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        return self.queryset.filter(loaner=self.kwargs.get("pk"))
