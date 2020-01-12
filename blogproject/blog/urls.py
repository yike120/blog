from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<pk>', views.ArticleDetailView.as_view(), name='detail'),
    path('comment/<pk>', views.comment, name='comment'),

    path('search/', views.SearchView.as_view(), name='search'),
    path('archive/<year>/<month>/', views.ArchiveView.as_view(), name='archive'),
    path('category/<pk>/', views.CategoryView.as_view(), name='category'),
    path('tag/<pk>/', views.TagView.as_view(), name='tag'),
]
