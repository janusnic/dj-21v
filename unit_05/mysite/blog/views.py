from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Article, Category
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

def article_detail(request,yy,mm,id):
    item = {'title':'Article Detail','content':id}    
    return render(request, "blog/article_detail.html", {'item':item})

def index(request):
    blog_list = Article.objects.order_by('-publish_date')
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

def news(request):
    blog_list = Article.objects.filter(category__name='news')
    context = {'blog_list': blog_list}
    return render(request, 'blog/index.html', context)

def detail0(request, blog_id):
    return HttpResponse("You're looking at article %s." % blog_id)

def detail1(request, blog_id):
    item = Article.objects.get(pk=blog_id)
    
    return render(request, 'blog/detail.html', {'item': item})

def detail(request, blog_id):
    try:
        item = Article.objects.get(pk=blog_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'blog/detail.html', {'item': item})

def detail(request, blog_id):
    item = get_object_or_404(Article, pk=blog_id)
    return render(request, 'blog/detail.html', {'item': item})

def vote(request, blog_id):
    return HttpResponse("You're voting on article %s." % blog_id)    
