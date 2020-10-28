
from colorhash import ColorHash
from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
from django.db.models import (Count, Q, Exists, OuterRef, 
                              F, Case, When, Value, Prefetch)


from squad.models import Player
from blog.mixins import LikedDislikedByMixin


class BlogManager(models.Manager):
    pass


class BlogQueryset(models.QuerySet):

    def with_likes(self):
        """
        Count likes/dislikes
        """
        qs = self.prefetch_related(
            Prefetch('comments', queryset=Comment.objects.with_likes())
        )
        qs = qs.annotate(likes_total=Count('likes', filter=Q(likes__dislike=False)))
        qs = qs.annotate(dislikes_total=Count('likes', filter=Q(likes__dislike=True)))
        
        return qs

class Blog(LikedDislikedByMixin, models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    text = RichTextUploadingField(blank=False, null=False)
    image = models.ImageField(upload_to='blogs/', blank=False, null=False)
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=False, 
        null=True
    )
    created = models.DateTimeField(auto_now=True)
    posted = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey('blog.Category', on_delete=models.CASCADE)

    objects = BlogManager.from_queryset(BlogQueryset)()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-posted']

    @property
    def comments_total(self):
        return self.comments.count()


class Category(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.name


class CommentManager(models.Manager):
    pass


class CommentQueryset(models.QuerySet):

    def with_likes(self):
        """
        Count likes/dislikes
        """

        qs = self.annotate(likes_total=Count('likes', filter=Q(likes__dislike=False)))\
        .annotate(dislikes_total=Count('likes', filter=Q(likes__dislike=True)))
        return qs


class Comment(LikedDislikedByMixin, models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=False, 
        null=True
    )
    text = models.TextField(blank=False, null=False)
    posted = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    post = models.ForeignKey(
        Blog, 
        on_delete=models.SET_NULL, 
        blank=False, 
        null=True,
        related_name='comments'
    )

    objects = CommentManager.from_queryset(CommentQueryset)()

    def __str__(self):
        return self.text[:30]

    @property
    def author_color(self):
        """Hash function that returns color from user's username and date_joined"""
        c = ColorHash(self.author.username)
        return c.hex


class Like(models.Model):

    author = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=False, 
        null=True
    )

    post = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='likes'
    )
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        related_name='likes'
    )

    dislike = models.BooleanField(default=False)

    class Meta:
        # One like per Post/Comment
        unique_together = ('author', 'post')
