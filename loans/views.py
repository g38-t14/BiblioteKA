from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

from copies.models import Copy
from books.models import Book

from .permissions import IsLoanOwner
from .serializers import LoanSerializer, ReturnLoanSerializer
from .models import Loan

from following.tasks import notify_followers


class LoanView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_blocked:
            raise PermissionDenied("Usuário com débito de livros!")

        book_id = self.kwargs["id"]
        if not Book.objects.filter(id=book_id).exists():
            raise NotFound("Desculpe, não temos esse livro cadastrado!")

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

            serializer.save(loaner=user, return_date=return_date, copy=copy_obj)
        else:
            raise NotFound("Não temos mais unidades disponiveis desse livro")


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
            raise PermissionDenied("Livro já retornado")
        serializer.validated_data["returned"] = True

        copy = loan.copy
        copy.available = True
        copy.save()
        serializer.save()

        book_id = loan.copy.book.id
        notify_followers(book_id)


class LoanDetailView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Loan.objects.filter(loaner=user)


class LoanListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()


class LoanListDetailView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    authentication_classes = [JWTAuthentication]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def get_queryset(self):
        return self.queryset.filter(loaner=self.kwargs.get("pk"))
