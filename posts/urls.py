from django.urls import path
from .views import PostCreateView, PostVerifyView, PostReportView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('verify/', PostVerifyView.as_view(), name='post-verify'),
    path('report/', PostReportView.as_view(), name='post-report'),

]
