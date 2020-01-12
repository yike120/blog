from django import forms
from django.core.exceptions import ValidationError

from blog.models import Category, Article, Comment


# def validate_category_name(value):
#     if Category.objects.filter(name=value).exists():
#         raise ValidationError('该名称对应的类别已存在')
#
#
# class CategoryForm(forms.Form):
#     name = forms.CharField(label='名称', max_length=32, validators=[validate_category_name])
#     age = forms.IntegerField(label='年龄', required=False)


class CategoryModelForm(forms.ModelForm):
    age = forms.IntegerField(label='年龄', required=False)

    class Meta:
        model = Category
        fields = ['name']


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = []


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
