from django.contrib import admin


from blog.models import Blog, Category, Comment, Like


class CommentInline(admin.TabularInline):
    model = Comment
    min_num = 0

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'snippet', 'created', 'posted')

    inlines = [CommentInline, ]

    def snippet(self, obj):
        return obj.text[:30]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class Like(admin.ModelAdmin):
    pass
