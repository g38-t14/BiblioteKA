from django.urls import path
from following.views import FollowView, FollowDetailView


urlpatterns = [
    path("book/<int:pk>/following/", FollowView.as_view()),
    path("following/", FollowView.as_view()),
    path("users/following/", FollowDetailView.as_view()),
]
