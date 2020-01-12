from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, FormView, CreateView

from blog.forms import CommentForm
from .models import Article


def index(request):
    # ?page=1
    # https://docs.djangoproject.com/zh-hans/2.1/topics/pagination/
    page = request.GET.get('page')
    article_list = Article.objects.all()
    paginator = Paginator(article_list, settings.PER_PAGE)
    article_list = paginator.get_page(page)
    context = {'article_list': article_list}
    return render(request, 'blog/index.html', context=context)


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 2


def detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increase_views()
    return render(request, 'blog/detail.html', {
        'article': article})


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog/detail.html'

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response


@login_required
def comment(request, pk):
    article = get_object_or_404(Article, pk=pk)
    title = f'{article.title}-评论'
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.article = article
            form.instance.user = request.user
            form.save()
            messages.add_message(request, messages.SUCCESS, '评论成功')
            return redirect(article)
    return render(request, 'forms.html', locals())


@method_decorator(login_required, name='dispatch')
class CommentView(CreateView):
    form_class = CommentForm
    template_name = 'forms.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_article(self):
        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)
        return article

    def get_context_data(self, **kwargs):
        article = self.get_article()
        context_data = super(CommentView, self).get_context_data(**kwargs)
        context_data.update({'title': f'{article}-留言'})
        return context_data

    def form_valid(self, form):
        form = self.get_form()
        form.instance.user = self.request.user
        form.instance.article = self.get_article()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.kwargs.get('pk')})


def search(request):
    q = request.GET.get('q')
    article_list = Article.objects.filter(
        Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q))
    return render(request, 'blog/index.html', {'article_list': article_list})


class SearchView(IndexView):

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        return super(SearchView, self).get_queryset().filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q))


def archive(request, year, month):
    article_list = Article.objects.filter(
        created_time__year=year, created_time__month=month)
    return render(request, 'blog/index.html', {'article_list': article_list})


class ArchiveView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchiveView, self).get_queryset().filter(
            created_time__year=year, created_time__month=month
        )


def category(request, pk):
    article_list = Article.objects.filter(category__pk=pk)
    return render(request, 'blog/index.html', {'article_list': article_list})


class CategoryView(IndexView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return super(CategoryView, self).get_queryset().filter(category__pk=pk)


def tag(request, pk):
    article_list = Article.objects.filter(tags__pk=pk)
    return render(request, 'blog/index.html', {'article_list': article_list})


class TagView(IndexView):
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return super(TagView, self).get_queryset().filter(tags__pk=pk)
