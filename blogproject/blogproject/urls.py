"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from blog.feeds import AllPostsRssFeed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('users.urls')),
    path('class/', include('blog.class_urls')),
    path('article/', include('blog.article_urls')),
    path('all/rss/', AllPostsRssFeed(), name='rss'),
]
#
# Django2.0自带的PathConveter包括:
# str：匹配除了路径分隔符（/）之外的非空字符串，如果没有转换器，默认使用str作为转换器。
# int：匹配0及正整数。
# slug：匹配字母、数字以及横杠、下划线组成的字符串。
# uuid：匹配格式化的uuid，如 075194d3-6885-417e-a8a8-6c931e272f00。
# path：匹配任何非空字符串，包含了路径分隔符（/）
