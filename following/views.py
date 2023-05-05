from django.shortcuts import render
from rest_framework import generics
from .models import Follower
from .serializers import FollowerSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class FollowView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


class FollowDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        return Follower.objects.filter(user_id=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
