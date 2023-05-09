from rest_framework import generics
from utils.generic_set_views import CreateDestroyGenericView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmployee

from .models import Follower
from books.models import Book
from .serializers import FollowerSerializer

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ParseError, NotFound


class FollowView(CreateDestroyGenericView, generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmployee]

    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        user = self.request.user
        book_id = self.kwargs["pk"]

        if user.user_book_follower.filter(book_id=book_id):
            raise ParseError("This book is already being followed!")

        book_obj = get_object_or_404(Book, pk=book_id)
        serializer.save(user=user, book=book_obj)

    def perform_destroy(self, instance):
        user = self.request.user
        book_id = self.kwargs["pk"]

        if not user.user_book_follower.filter(book_id=book_id):
            raise NotFound("This book is not being followed!")

        follow_obj = get_object_or_404(
            Follower, book_id=self.kwargs.get("pk"), user=user
        )
        follow_obj.delete()


class FollowDetailView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def get_queryset(self):
        user = self.request.user

        return Follower.objects.filter(user=user)
