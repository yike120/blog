import os
import django
from django.db.models import Count

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings')
    django.setup()
    from blog.models import Category

    results = Category.objects.annotate(num_articles=Count('article')).filter(num_articles__gt=0)
    for result in results:
        print(result, result.num_articles)
