from django.contrib import admin


from blog.models import Blog, Category


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'snippet', 'created', 'posted')

    def snippet(self, obj):
        return obj.text[:30]



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
