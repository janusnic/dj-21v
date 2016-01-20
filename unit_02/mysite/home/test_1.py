# -*- coding: utf-8 -*-
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from home.views import home_page 

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') 
        self.assertEqual(found.func, home_page) 

    def test_home_page_returns_correct_html(self):

        # создали HttpRequest object, который использует Django когда пользователь запрашивает страницу.

        request = HttpRequest()  
        
        # перенаправляем запрос на метод home_page view, который формирует response - экземпляр класса HttpResponse. Далее проверяем является ли .content в response HTML-текстом который мы отдаем пользователю.

        response = home_page(request)  
        
        # HTML-текст должен начинаться с html тега, который должен закрываться вконце. response.content является сырым литералом (raw bytes), а не Python-строкой, поэтому мы используем b'' синтаксис.

        self.assertTrue(response.content.startswith(b'<html>'))  
        
        # Мы хотим поместить тег title, содержащий наш заголовок.

        self.assertIn(b'<title>Welcome to Django. This is my cool Site!</title>', response.content)  
        self.assertTrue(response.content.endswith(b'</html>'))  