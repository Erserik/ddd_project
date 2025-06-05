from rest_framework import generics, permissions
from .models import Post
from .serializers import PostCreateSerializer
from .utils import extract_text_from_file
from .blockchain_utils import save_to_blockchain, is_hash_recorded
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import hashlib, json
import numpy as np
from sentence_transformers import SentenceTransformer, util
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

model = SentenceTransformer('all-MiniLM-L6-v2')

class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Создание поста с ML-анализом и записью в 'блокчейн'",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'type'],
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'type': openapi.Schema(type=openapi.TYPE_STRING, enum=['text', 'image', 'document']),
                'content': openapi.Schema(type=openapi.TYPE_STRING),
                'image': openapi.Schema(type=openapi.TYPE_FILE),
                'document': openapi.Schema(type=openapi.TYPE_FILE),
            }
        )
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        post_type = self.request.data.get('type')
        text_data = ""

        if post_type == 'document':
            file = self.request.FILES['document']
            text_data = extract_text_from_file(file, file.name)
        elif post_type == 'text':
            text_data = self.request.data.get('content', '')
        elif post_type == 'image':
            text_data = self.request.FILES['image'].read()

        text_bytes = text_data.encode('utf-8') if isinstance(text_data, str) else text_data
        sha256_hash = hashlib.sha256(text_bytes).hexdigest()

        embedding = None
        similarity = 0.0
        status = "original"

        if post_type in ['text', 'document'] and text_data.strip():
            new_embedding = model.encode(text_data, convert_to_tensor=True).cpu()
            all_posts = Post.objects.exclude(embedding__isnull=True)
            max_sim = 0.0

            for post in all_posts:
                try:
                    if not post.embedding:
                        continue
                    existing = json.loads(post.embedding)
                    existing_tensor = np.asarray(existing, dtype=np.float32)
                    sim = float(util.cos_sim(new_embedding, existing_tensor).item())
                    if sim > max_sim:
                        max_sim = sim
                except Exception as e:
                    continue

            similarity = round(max_sim, 4)
            if similarity > 0.9:
                status = "duplicate"
            elif similarity > 0.6:
                status = "suspicious"
            embedding = json.dumps(new_embedding.tolist())

        serializer.save(
            user=self.request.user,
            content=text_data if isinstance(text_data, str) else '',
            sha256_hash=sha256_hash,
            status=status,
            similarity_score=similarity,
            embedding=embedding
        )

        # Сохраняем в "блокчейн"
        save_to_blockchain(sha256_hash, self.request.user.username, serializer.validated_data.get('title'))


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Post


class PostVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hash_to_check = request.query_params.get('hash')
        if not hash_to_check:
            return Response({"error": "Hash parameter is required."}, status=400)

        post = Post.objects.filter(sha256_hash=hash_to_check).order_by('-created_at').first()


        if post:
            return Response({
                "exists": True,
                "title": post.title,
                "user": post.user.username,
                "created_at": post.created_at,
                "document_url": request.build_absolute_uri(post.document.url) if post.document else None,
            })
        return Response({"exists": False})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from django.conf import settings
from .models import Post
from .pdf_utils import generate_report_pdf
import os

class PostReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hash_to_check = request.query_params.get("hash")
        if not hash_to_check:
            return Response({"error": "Hash parameter is required."}, status=400)

        post = Post.objects.filter(sha256_hash=hash_to_check).order_by("-created_at").first()
        if not post:
            return Response({"error": "Report not found. Try re-uploading the post."}, status=404)

        # Путь к PDF
        import os
        from django.conf import settings

        pdf_path = os.path.join(settings.MEDIA_ROOT, "reports", f"report_{post.sha256_hash}.pdf")

        # Генерация, если не существует
        if not os.path.exists(pdf_path):
            generate_report_pdf(post)

        #  Отдаём файл
        return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")