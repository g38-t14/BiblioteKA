from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsEmployeeOrReadOnly
from .models import Book
from .serializers import BookSerializer
from copies.models import Copy


class BookView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeOrReadOnly]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        book_obj = serializer.save()

        for num_copies in range(book_obj.quantity):
            Copy.objects.create(book=book_obj)

        return book_obj
