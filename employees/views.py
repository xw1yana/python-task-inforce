from rest_framework import generics, permissions

from .serializers import EmployeeRegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = EmployeeRegisterSerializer
    permission_classes = [permissions.AllowAny]
