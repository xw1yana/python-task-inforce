from rest_framework import serializers

from .models import Employee


class EmployeeRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Employee
        fields = ("id", "username", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Employee(**validated_data)
        user.set_password(password)
        user.save()
        return user
