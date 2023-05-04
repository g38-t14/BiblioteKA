from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from copies.models import Copy
from .serializers import LoanSerializers
from .models import Loan
from books.models import Book
from rest_framework.exceptions import NotFound, PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta


class LoanView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializers


    def perform_create(self, serializer):

        user = self.request.user
        if user.is_blocked:
            raise PermissionDenied("Usuário com débito de livros!")
       
        book_id = self.kwargs["id"]
        book_obj = get_object_or_404(Book, pk=book_id)
        copy_obj = Copy.objects.filter(book = book_obj, available=True).first()
    
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
            raise NotFound(
                "Não temos mais unidades disponiveis desse livro"
            )
    



