from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# login schema
token_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль')
    },
    required=['username', 'password']
)

# logout schema
logout_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh токен')
    },
    required=['refresh']
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path(
        'login/',
        swagger_auto_schema(
            method='post',
            operation_description="Вход пользователя",
            request_body=token_schema,
            responses={
                200: openapi.Response(
                    description="Успешный вход",
                    examples={
                        "application/json": {
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci...",
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGci..."
                        }
                    }
                ),
                401: "Неверные данные"
            }
        )(TokenObtainPairView.as_view()),
        name='token_obtain_pair'
    ),
    #path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        'logout/',
        swagger_auto_schema(
            method='post',
            operation_description="Выход пользователя (блокировка токена)",
            request_body=logout_schema,
            responses={205: "Успешный выход"}
        )(TokenBlacklistView.as_view()),
        name='token_blacklist'
    )
]
