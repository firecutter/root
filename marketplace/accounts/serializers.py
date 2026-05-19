# 📁 Caminho: root/marketplace/accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer de leitura — retorna dados públicos do usuário."""

    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "user_type", "phone")
        read_only_fields = ("id",)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer de cadastro — cria um novo usuário com senha hasheada."""

    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "phone",
            "password",
            "password_confirm",
        )

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError({"password": "As senhas não conferem."})
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer de login — valida credenciais e retorna o objeto User."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # AbstractUser com USERNAME_FIELD = 'email' → authenticate espera username=email
        user = authenticate(username=data["email"], password=data["password"])
        if not user:
            raise serializers.ValidationError("E-mail ou senha inválidos.")
        if not user.is_active:
            raise serializers.ValidationError("Conta desativada.")
        data["user"] = user
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer para troca de senha autenticada."""

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["new_password_confirm"]:
            raise serializers.ValidationError({"new_password": "As senhas não conferem."})
        return data