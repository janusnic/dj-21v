from django.shortcuts import get_object_or_404, render
from .models import Article, Category, Tag
import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import time
from calendar import month_name

def latest(request):
    items = Article.objects.filter(title__startswith='QuerySet').filter(publish_date__gte=datetime.date(2015, 1, 1))

    return render(request, "blog/special_case_2016.html", {'items':items})

def index(request):

    blog_list = Article.objects.order_by('-publish_date')
    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')

    context = {'categories_list':category_list, 'blog_list': blog_list , 'tags_name':tags_name, 'months':monthly_archive_list()}

    return render(request, 'blog/index.html', context)

def news(request):
    blog_list = Article.objects.filter(category__name='news')
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

def detail(request, postslug):

    result = get_object_or_404(Article, slug=postslug)
    try:
        result.views = result.views + 1
        result.save()
    except:
        pass
    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')

    return render(request, 'blog/detail.html', {'categories_list':category_list, 'item': result, 'tags_name':tags_name, 'months':monthly_archive_list()})

def category(request, categoryslug):
    name = Category.objects.get(slug=categoryslug)
    posts = Article.objects.filter(category=name)
    category_list = Category.objects.order_by('name')
    context = {'categories_list':category_list, 'blog_list': posts}
    return render(request, 'blog/singlecategory.html', context)

def tags(request):
    tags_name = Tag.objects.order_by('name')

    context = {'tags_name':tags_name}
    return render(request, 'blog/singlecategory.html', context)

def monthly_archive_list():
    """Make a list of months to show archive links."""

    if not Article.objects.count(): return []

    # set up vars
    year, month = time.localtime()[:2]
    first = Article.objects.order_by("created_date")[0]
    fyear = first.created_date.year
    fmonth = first.created_date.month
    months = []

    # loop over years and months
    for y in range(year, fyear-1, -1):
        start, end = 12, 0
        if y == year: start = month
        if y == fyear: end = fmonth-1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months

def monthly_archive(request, year, month):
    """Monthly archive."""

    posts = Article.objects.filter(created_date__year=year, created_date__month=month)

    paginator = Paginator(posts, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    return render(request,"blog/month_archive.html",dict(blog_list=posts, months=monthly_archive_list(), archive=True))
