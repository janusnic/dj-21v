from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

def req_test(request): 
    output = "<html><title>Welcome to Django.</title><body><p>This is Request Test!</p>"

    

    mess = request.scheme
    output += 'scheme = '+ mess + '<br>'
    mess = str(request.body)
    output += 'body = '+ mess + '<br>'
    mess = request.path
    output += 'path = '+ mess + '<br>'
    mess = request.path_info
    output += 'path_info = '+ mess + '<br>'
    
    if request.method == 'GET':
        mess = 'Method = '+'GET' + '<br>'
    elif request.method == 'POST':
        mess = 'Method = '+'POST' + '<br>'
    output += mess
    # request.encoding = 'utf-8'
    mess = settings.DEFAULT_CHARSET
    output += 'DEFAULT_CHARSET = '+ mess + '<br>'
    mess = str(request.encoding)
    output += 'encoding = '+ mess + '<br>'
    mess = request.META['HTTP_ACCEPT_ENCODING']
    output += 'HTTP_ACCEPT_ENCODING = '+ mess + '<br>'

    if request.user.is_authenticated():
        mess = 'Hi User'
    else:
        mess = 'Hi Anonimouse!'

    output += 'User = '+ mess + '<br>'
    output += 'Host = '+ request.get_host() + '<br>'
    output += 'Path = '+ request.get_full_path() + '<br>'


    output += "</body></html>"
    response = HttpResponse(output)
    # response = HttpResponse(output, content_type='application/vnd.ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    response['Age'] = 120 # Установка заголовков
    print(response.charset)
    print(response.status_code) # 200
    print(response.reason_phrase) # OK
    print(response.content)
    print(response.getvalue())
   

    return response

    # return HttpResponse(output)

class Myobject:
    attribute = 'my_object.attribute'

def home_page(request):
    # return render(request, 'home/home.html')
    my_dict = {'key':'My dikt Key'}
    my_object = Myobject()

    my_list = [1,2,3,4]
    categories = [{'id':0,'name':'Python'},{'id':1,'name':'Django'},{'id':2,'name':'Web'},{'id':4,'name':'Javascript'}]
    
    cities = [
    {'name': 'Mumbai', 'population': '19,000,000', 'country': 'India'},
    {'name': 'Calcutta', 'population': '15,000,000', 'country': 'India'},
    {'name': 'New York', 'population': '20,000,000', 'country': 'USA'},
    {'name': 'Chicago', 'population': '7,000,000', 'country': 'USA'},
    {'name': 'Tokyo', 'population': '33,000,000', 'country': 'Japan'},
    ]

    return render(request, 'home/home.html', {'first_name': 'Billi', 'last_name': 'Bons', 'my_dict':my_dict,'my_list':my_list,'my_object':my_object, 'name':'<script>alert("XSS");</script>','rowclass1':'border: red solid 7px;', 'rowclass2':'border: green solid 3px;','categories':categories,'cities':cities})
 

def exampl1(request):
    articles = [{'id':0,'name':'Python'},{'id':1,'name':'Django'},{'id':2,'name':'Web'},{'id':4,'name':'Javascript'}]
    return render(request, "home/exampl1.html", {'articles':articles})

def article(request,id):
    item = {'title':1,'content':id}    
    return render(request, "home/article.html", {'item':item})

def home(request):
    return render(request, "home/index.html", {})