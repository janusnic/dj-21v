from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# home_page = None

# def home_page():
def home_page(request): 
    # return HttpResponse()
    # return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title>")
    return HttpResponse("<html><title>Welcome to Django. This is my cool Site!</title></html>")
#    pass
 
def home(request):
    return render(request, "home/index.html", {})