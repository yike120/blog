from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import ArticleModelForm
from .models import Article


def article_list(request):
    q = request.GET.get('q', '')
    page = request.GET.get('page')
    article_list = Article.objects.filter(Q(title__contains=q) | Q(content__contains=q))
    paginator = Paginator(article_list, 5)
    article_list = paginator.get_page(page)
    context = {'article_list': article_list}
    return render(request, 'demo/article_list.html', context=context)


def article_add(request):
    if request.method == 'GET':
        form = ArticleModelForm()
    else:
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, '添加成功,你可以继续添加')
            return redirect('article:article_list')
    return render(request, 'demo/article_form.html', {'form': form})


def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        form = ArticleModelForm(instance=article)
    else:
        form = ArticleModelForm(request.POST, instance=article)
        if form.is_valid():
            messages.add_message(request, messages.INFO, '编辑成功，你可以继续编辑')
            form.save()
            return redirect('article:article_list')
    return render(request, 'demo/article_form.html', {'form': form})


def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    messages.add_message(request, messages.SUCCESS, '数据已删除')
    return redirect('article:article_list')
