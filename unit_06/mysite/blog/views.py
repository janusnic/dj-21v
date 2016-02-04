from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Article, Category, Tag
import datetime

def special_case_2016(request):
    items = Article.objects.filter(publish_date__year=2016)  
    return render(request, "blog/special_case_2016.html", {'items':items})

def latest(request):
    items = Article.objects.filter(title__startswith='QuerySet').filter(publish_date__gte=datetime.date(2015, 1, 1))  
    
    return render(request, "blog/special_case_2016.html", {'items':items})

def year_archive(request,yy):
    item = {'title':'Year Archive','content':yy}    
    return render(request, "blog/year_archive.html", {'item':item})

def month_archive(request,yy,mm):
    item = {'title':'Month Archive','content':yy}    
    return render(request, "blog/month_archive.html", {'item':item})


def index(request):

    blog_list = Article.objects.order_by('-publish_date')

    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')
    
    context = {'categories_list':category_list, 'blog_list': blog_list , 'tags_name':tags_name}
    #context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

def news(request):
    blog_list = Article.objects.filter(category__name='news')
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

def detail(request, postslug):
    # result = Article.objects.get(slug=postslug)
    result = get_object_or_404(Article, slug=postslug)
    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')
            
    return render(request, 'blog/detail.html', {'categories_list':category_list, 'item': result, 'tags_name':tags_name})

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