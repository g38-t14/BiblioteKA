from rest_framework.views import Request, Response

from rest_framework.mixins import CreateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView


class CreateDestroyGenericView(CreateModelMixin, DestroyModelMixin, GenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request: Request, *args: tuple, **kwargs: dict) -> Response:
        return super().destroy(request, *args, **kwargs)

