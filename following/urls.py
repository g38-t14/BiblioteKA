from django.urls import path
from .views import FollowView, FollowDetailView


urlpatterns = [
    path("book/<int:pk>/following/", FollowView.as_view()), #Create Follow // Delete Follow
    path("following/", FollowView.as_view()), 
    path("users/<int:pk>/following/", FollowDetailView.as_view()), #List user's follows
]
