from django.urls import path
from blog.views import BlogListView, BlogDetailView, CreateCommentView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<int:pk>/comment/', CreateCommentView.as_view(), name='comment'),
]