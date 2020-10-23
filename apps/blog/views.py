from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, FileResponse, HttpResponse
from django.db import transaction
from django.urls import reverse

from blog.models import Blog, Comment
from blog.forms import BlogCommentForm


class BlogListView(ListView):
    template_name = 'blog/blog_list.html'

    def get_queryset(self):
        return Blog.objects.filter(posted__lte=timezone.localtime(timezone.now()))


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        post = self.get_object()

        context['next_post'] = Blog.objects.filter(posted__gt=post.posted).order_by('posted').first()
        context['prev_post'] = Blog.objects.filter(posted__lt=post.posted).order_by('posted').first()
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
    