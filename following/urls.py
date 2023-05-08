from django.urls import path
from .views import FollowView, FollowDetailView


urlpatterns = [
    path(
        "book/<int:pk>/following/", FollowView.as_view()
    ),  # Criar Follow | Deletar Follow (Unfollow)
    path("following/", FollowView.as_view()),  # Listar Todos Follows (só employee)
    path("users/following/", FollowDetailView.as_view()),  # Listar Follows do Usuário
]
