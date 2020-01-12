from django import template
from django.db.models import Count

from blog.models import Article, Category, Tag

register = template.Library()


@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all()[:num]


@register.simple_tag
def get_archives():
    return Article.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(
        num_articles=Count('article')).filter(num_articles__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
