import markdown
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

from users.models import User

# 用户：id, 昵称 邮箱 密码
# 分类：id, 名称
# 标签：id, 名称
# 文章：id, user, 阅读次数, 标题, 内容,  摘录(对内容的简介), 创建时间
# 评论：id, user, 文章, 内容, 创建时间

MD = markdown.Markdown(extensions=[
    'markdown.extensions.extra',
    'markdown.extensions.codehilite',
    TocExtension(slugify=slugify),
])


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name='名称', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    title = models.CharField(max_length=64, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    excerpt = models.CharField(max_length=128, blank=True, verbose_name='摘要')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='类别')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    @staticmethod
    def get_md():
        return markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TocExtension(slugify=slugify),
        ])

    def md_content(self):
        md = self.get_md()
        return md.convert(self.content)

    def md_toc(self):
        md = self.get_md()
        md.convert(self.content)
        return md.toc

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = self.get_md()
            self.excerpt = strip_tags(md.convert(self.content))[:128]
        super(Article, self).save(*args, **kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})


# on_delete 说明
# https://docs.djangoproject.com/zh-hans/2.1/ref/models/fields/#django.db.models.ForeignKey


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='文章')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
