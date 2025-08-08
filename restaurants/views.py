from datetime import date

from django.utils import timezone
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Menu, Restaurant, Vote
from .serializers import MenuSerializer, RestaurantSerializer, VoteSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TodayMenuList(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Menu.objects.filter(date=date.today())


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        menu = serializer.validated_data["menu"]
        vote_date = menu.date
        existing = Vote.objects.filter(
            employee=self.request.user, vote_date=vote_date
        ).first()
        if existing:
            from rest_framework.exceptions import ValidationError

            raise ValidationError("You already voted today.")
        serializer.save(employee=self.request.user, vote_date=vote_date)


class TodayResultsView(generics.ListAPIView):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Vote.objects.filter(vote_date=date.today())
