from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    """
    password = serializers.CharField(write_only=True, help_text="Пароль для входа")

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True, 'help_text': 'Email пользователя'}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
