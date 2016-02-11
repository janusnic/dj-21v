from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Article, Category, Tag
import datetime

from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
import time
from calendar import month_name

from .forms import UserForm, UserProfileForm

from django.contrib.auth import authenticate, login

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

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

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'blog/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the email and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the email/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
            # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/blog/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Blog account is disabled.")
        else:
       # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        # return render(request, 'blog/login.html', {})
        return render(request, 'blog/index.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/blog/')
