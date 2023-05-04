from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from .permissions import IsLoanOwner
from .serializers import LoanSerializers


class ReturnBookView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsLoanOwner]
    serializer_class = LoanSerializers
    lookup_field = "loan_id"
