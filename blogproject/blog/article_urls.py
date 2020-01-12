from django.urls import path

from . import article_views

app_name = 'article'
urlpatterns = [
    path('list', article_views.article_list, name='article_list'),
    path('add', article_views.article_add, name='article_add'),
    path('update/<pk>', article_views.article_update, name='article_update'),
    path('delete/<pk>', article_views.article_delete, name='article_delete'),
]
