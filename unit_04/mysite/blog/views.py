from django.shortcuts import render
from .models import Article

def special_case_2016(request):
    item = {'title':'Special Case 2016','topics':10}    
    return render(request, "blog/special_case_2016.html", {'item':item})

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

def latest(request):
    latest_blog_list = Article.objects.order_by('-publish_date')[:10]
    context = {'latest_blog_list': latest_blog_list}
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
