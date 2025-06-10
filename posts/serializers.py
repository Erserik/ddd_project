from rest_framework import serializers
from .models import Post

class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'type', 'content', 'image', 'document',
            'status', 'similarity_score', 'sha256_hash'
        ]
        read_only_fields = ['status', 'similarity_score', 'sha256_hash']

    def validate(self, data):
        post_type = data.get('type')

        if post_type == 'text' and not data.get('content'):
            raise serializers.ValidationError("Поле 'content' обязательно для текстового поста.")
        elif post_type == 'image' and not data.get('image'):
            raise serializers.ValidationError("Загрузите изображение.")
        elif post_type == 'document' and not data.get('document'):
            raise serializers.ValidationError("Загрузите документ.")
        elif post_type not in ['text', 'image', 'document']:
            raise serializers.ValidationError("Недопустимый тип поста.")
        return data

# serializers.py

from .models import Vote, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']
