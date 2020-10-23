from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, FileResponse, HttpResponse
from django.db import transaction

from blog.models import Blog


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
        return context
