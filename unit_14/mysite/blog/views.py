from django.shortcuts import get_object_or_404, render, redirect
from .models import Article, Category, Tag, Comment
import datetime
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import time
from calendar import month_name

from django.views.generic import CreateView

from .forms import CommentForm

from django.contrib import messages

from markdown import markdown

from django.views.generic import ListView


def latest(request):
    items = Article.objects.filter(title__startswith='QuerySet').filter(publish_date__gte=datetime.date(2015, 1, 1))

    return render(request, "blog/special_case_2016.html", {'items':items})

def index(request):

    blog_list = Article.objects.order_by('-publish_date')
    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')

    context = {'categories_list':category_list, 'blog_list': blog_list , 'tags_name':tags_name, 'months':monthly_archive_list()}

    return render(request, 'blog/index.html', context)

class HomeView(ListView):
    template_name = 'blog/news.html'
    queryset = Article.objects.order_by('-created_date')


class ArticleDetail(CreateView):
    model = Article
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    def dispatch(self, *args, **kwargs):
        return super(ArticleDetail, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
 
        # instance.user = self.request.user
        #instance.author_name = self.request.user.username

        if form['parent'].value() == '':
            instance.user = self.request.user
            instance.author_name = self.request.user.username
            
        else:
            parent = Comment.objects.get(id=int(form['parent'].value()))
            instance.parent = parent
            
            instance.user = self.request.user
            instance.author_name = self.request.user.username
            instance.depth = parent.depth + 1
            
            instance.path = parent.path
            

        instance.save()
        
        return super(ArticleDetail, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['article'] = self.get_object()
        return kwargs
    
    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        articlec = self.get_object()
        d['comment_tree'] = Comment.objects.select_related().filter(article=articlec).order_by('path') 
        d['article'] = self.get_object()
        return d

    def get_success_url(self):
        return self.get_object().get_absolute_url()


def detail(request, postslug):

    result = get_object_or_404(Article, slug=postslug)
    try:
        result.views = result.views + 1
        result.save()
    except:
        pass

    category_list = Category.objects.order_by('name')
    tags_name = Tag.objects.order_by('name')
    
    return render(request, 'blog/detail.html', locals())
    

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
