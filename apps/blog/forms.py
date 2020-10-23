from django import forms
from django.forms import ModelForm, Textarea
from blog.models import Comment


class BlogCommentForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Comment
        fields = ['text']
