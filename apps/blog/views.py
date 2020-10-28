from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, FileResponse, HttpResponse, HttpResponseRedirect
from django.db import transaction, models
from django.urls import reverse
from django.db.models import (Count, Q, Exists, OuterRef, 
                              F, Case, When, Value)

from blog.models import Blog, Comment, Like, Category
from blog.forms import BlogCommentForm


class BlogListView(ListView):
    template_name = 'blog/blog_list.html'
    paginate_by = 9
    search_fields = ['id', ]
    text_search_fields = ['title', 'text', 'author__first_name', 'author__last_name',
                          'author__username']

    def get_queryset(self):
        user = self.request.user

        qs = Blog.objects.all()
        qs = qs.filter(posted__lte=timezone.localtime(timezone.now())).order_by('-posted')
        qs = qs.with_likes()

        qs = self._get_searched_queryset(qs)

        return qs

    def _get_searched_queryset(self, queryset):
        search_string = self.request.GET.get('query', None)
        print(search_string)
        if search_string:
            q_condition = None
            if search_string.isdigit():
                for field in self.search_fields:
                    if q_condition:
                        q_condition |= Q(**{'{}'.format(field): search_string})
                    else:
                        q_condition = Q(**{'{}'.format(field): search_string})
                queryset = queryset.filter(q_condition)
            for field in self.text_search_fields:
                if q_condition:
                    q_condition |= Q(**{'{}__icontains'.format(field): search_string})
                else:
                    q_condition = Q(**{'{}__icontains'.format(field): search_string})
            queryset = queryset.filter(q_condition)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['categories'] = Category.objects.all()
        return context

class BlogDetailView(DetailView):
    template_name = 'blog/blog_detail.html'

    def get_queryset(self):
        user = self.request.user
        qs = Blog.objects.with_likes()\
            .filter(posted__lte=timezone.localtime(timezone.now()))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()

        context['next_post'] = Blog.objects.filter(posted__gt=post.posted).order_by('posted').first()
        context['prev_post'] = Blog.objects.filter(posted__lt=post.posted).order_by('-posted').first()
        context['comment_form'] = BlogCommentForm(self.request.POST or None)
        return context


class CreateCommentView(LoginRequiredMixin, CreateView):
    fields = ['text',]
    model = Comment

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.object.post.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        blog = Blog.objects.get(id=self.kwargs['pk'])
        form.instance.post = blog
        return super().form_valid(form)


class DeleteCommentView(LoginRequiredMixin, DeleteView):

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.object.post.pk})


class LikeDislikeView(LoginRequiredMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Like/dislike posts and comments"""

        user = self.request.user
        is_dislike = request.GET.get('type', None) == 'dislike'
        post_or_comment_id = self.kwargs['pk']
        is_comment = request.GET.get('comment', False)
        if is_comment:
            # Comment to like
            post_or_comment = Comment.objects.get(pk=post_or_comment_id)
            post_id = post_or_comment.post.pk
        else:
            # Post to like
            post_or_comment = Blog.objects.get(pk=post_or_comment_id)
            post_id = post_or_comment.pk

        like_qs = post_or_comment.likes.filter(author=user)
        if like_qs.exists():
            like_obj = like_qs.first()
            if like_obj.dislike == is_dislike:
                like_obj.delete()
            else:
                like_obj.dislike = is_dislike
                like_obj.save()
        else:
            like_obj = Like(dislike=is_dislike, author=user)
            if is_comment:
                like_obj.comment = post_or_comment
            else:
                like_obj.post = post_or_comment
            like_obj.save()
        

        return HttpResponseRedirect(reverse('blog-detail', kwargs={'pk': post_id}))
