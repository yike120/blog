from django.urls import path
from django.views.generic import TemplateView

from . import class_views

app_name = 'class'
urlpatterns = [
    path('view1', class_views.view1, name='view1'),
    path('view2', class_views.View2.as_view(), name='view2'),
    path('view3', class_views.View2.as_view(name='view3'), name='view3'),

    path('about1', class_views.about1, name='about1'),
    path('about2', class_views.About2.as_view(), name='about2'),
    path('about3', TemplateView.as_view(template_name='class/about.html'))
]
