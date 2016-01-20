# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

assert 'Django' in browser.title

print (browser.title)

try:
    
    WebDriverWait(browser, 10).until(EC.title_contains("Welcome"))

    # You should see "Welcome to Django This is my cool Site!"
    print (browser.title,' This is my cool Site!')

finally:
    browser.quit()