from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор платежей"""

    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["date", "session_id", "link", "user"]


class UserOwnerSerializer(serializers.ModelSerializer):
    """Сериализатор профиля для владельца"""

    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "password",
            "email",
            "phone",
            "first_name",
            "last_name",
            "payments",
        )


class UserGeneralSerializer(serializers.ModelSerializer):
    """Сериализатор профиля для всех зарегистрированных"""

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
        )


class UserModeratorSerializer(serializers.ModelSerializer):
    """Сериализатор профиля для модератора"""

    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "first_name",
            "last_name",
            "payments",
        )


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации"""

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )
