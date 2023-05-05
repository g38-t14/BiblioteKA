from django.urls import path
from .views import FollowView, FollowDetailView


urlpatterns = [
    path("following/", FollowView.as_view()),
    path("users/following", FollowView.as_view()),
    path("book/<int:pk>/following/", FollowDetailView.as_view())
]
