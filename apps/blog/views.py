from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, FileResponse, HttpResponse, HttpResponseRedirect
from django.db import transaction, models
from django.urls import reverse
from django.db.models import (Count, Q, Exists, OuterRef, 
                              F, Case, When, Value)

from blog.models import Blog, Comment, Like
from blog.forms import BlogCommentForm


class BlogListView(ListView):
    template_name = 'blog/blog_list.html'
    paginate_by = 9

    def get_queryset(self):
        user = self.request.user
        qs = Blog.objects.with_likes()\
            .filter(posted__lte=timezone.localtime(timezone.now()))

        if user.is_authenticated:
            qs = qs.with_liked_disliked(user)

        return qs

class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'

    def get_queryset(self):
        user = self.request.user
        qs = Blog.objects.with_likes()\
            .filter(posted__lte=timezone.localtime(timezone.now()))

        if user.is_authenticated:
            qs = qs.with_liked_disliked(user)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()

        context['next_post'] = Blog.objects.filter(posted__gt=post.posted).order_by('posted').first()
        context['prev_post'] = Blog.objects.filter(posted__lt=post.posted).order_by('-posted').first()
        context['comment_form'] = BlogCommentForm(self.request.POST or None)
        return context


class CreateCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text',]

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.object.post.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        blog = Blog.objects.get(id=self.kwargs['pk'])
        form.instance.post = blog
        return super().form_valid(form)
    

class LikeDislikeView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Like/dislike posts and comments"""

        user = self.request.user
        is_dislike = request.GET.get('type', None) == 'dislike'
        post_or_comment_id = self.kwargs['pk']
        if request.GET.get('comment', None):
            # Comment to like
            post_or_comment = Comment.objects.get(pk=post_or_comment_id)
        else:
            # Post to like
            post_or_comment = Blog.objects.get(pk=post_or_comment_id)

        like_qs = post_or_comment.likes.filter(author=user)
        if like_qs.exists():
            like_obj = like_qs.first()
            if like_obj.dislike == is_dislike:
                print('DELETING')
                like_obj.delete()
            else:
                like_obj.dislike = is_dislike
                like_obj.save()
        else:
            print('CREATING')
            like_obj = Like(dislike=is_dislike, author=user, content_object=post_or_comment)
            like_obj.save()

        return HttpResponseRedirect(reverse('blog-detail', kwargs={'pk': self.kwargs['pk']}))
