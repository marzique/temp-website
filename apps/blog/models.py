from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=500, null=False, blank=False)
    text = models.TextField(blank=False, null=False)
    image = models.ImageField(upload_to='blogs/', blank=False, null=False)
    created = models.DateTimeField(auto_now=True)
    posted = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey('blog.Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.name

