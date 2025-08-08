from django.utils import timezone
from rest_framework import serializers

from employees.serializers import EmployeeRegisterSerializer

from .models import Menu, Restaurant, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["id", "name", "description"]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "restaurant", "date", "items"]

    def validate(self, attrs):
        restaurant = attrs.get("restaurant")
        date = attrs.get("date")
        if Menu.objects.filter(restaurant=restaurant, date=date).exists():
            raise serializers.ValidationError(
                "Menu for this restaurant and date already exists."
            )
        return attrs


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "employee", "menu", "created_at", "vote_date"]
        read_only_fields = ["employee", "created_at", "vote_date"]

    def create(self, validated_data):
        return super().create(validated_data)
