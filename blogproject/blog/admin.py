from django.contrib import admin

# Register your models here.
from blog.models import Category, Tag, Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', 'author']


admin.site.register(Article, ArticleAdmin)
admin.site.register([Category, Tag, Comment])
