from django.urls import path

# posts/urls.py

from .views import (
    PostCreateView, PostVerifyView, PostReportView,
    PostDeleteView, PostVoteView,
    PostCommentsListView, PostCommentCreateView,
    CommentUpdateView, CommentDeleteView, PostListView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),

    path('create/', PostCreateView.as_view(), name='post-create'),
    path('verify/', PostVerifyView.as_view(), name='post-verify'),
    path('report/', PostReportView.as_view(), name='post-report'),

    # Новые пути:
    path('<int:pk>/vote/', PostVoteView.as_view(), name='post-vote'),
    path('<int:pk>/comments/', PostCommentsListView.as_view(), name='post-comments-list'),
    path('<int:pk>/comments/add/', PostCommentCreateView.as_view(), name='post-comments-create'),

    path('<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('comments/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
