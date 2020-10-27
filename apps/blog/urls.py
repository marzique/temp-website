from django.urls import path
from blog.views import (
    BlogListView, 
    BlogDetailView, 
    CreateCommentView,
    LikeDislikeView,
    DeleteCommentView
)

urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<int:pk>/comment/', CreateCommentView.as_view(), name='comment'),
    path('<int:pk>/comment/delete', DeleteCommentView.as_view(), name='delete-comment'),
    path('<int:pk>/react/', LikeDislikeView.as_view(), name='post-react'),
]