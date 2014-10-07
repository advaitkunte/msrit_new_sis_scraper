#!/usr/bin/python

import random
import math
import urllib
import urllib2
from bs4 import BeautifulSoup
import base64,cookielib

username = ""
password = ""

url = 'http://parents.msrit.edu/index.php'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# to get first cookie and other parameters
response = opener.open(url)

token = []
val = ''
bs = BeautifulSoup(response.read())
table = bs.find("table").find('tr').findAll('input')

val = table[len(table)-3].get('value')
token.append(table[len(table)-1].get('name'))
token.append(table[len(table)-1].get('value'))

def anotherfunction():
    n = math.floor(random.random()*62)
    n = int(n)
    if(n<10):
        return n
    if(n<36):
        return chr(n+55)
    return chr(n+61)

def randomstring(L):
    s = ''
    while(len(s)<L):
        s += str(anotherfunction())
    return s

tmp = []

randsting = ''
for i in range(0,len(password)):
    randsting += password[i]+randomstring(2)

# getting encoded password
encoded = base64.standard_b64encode(randsting)

# building the POST param
values = {
          'username' : username,
          'password' : encoded,
          'passwd' : encoded,
          'option' : 'com_user',
          'task' : 'login',
          'remember' : 'No',
          'return' : val,
          'return' : '',
          token[0] : token[1]
          }
data = urllib.urlencode(values)
# getting login cookie
response = opener.open(url, data)
url = response.geturl()


values = { 'option' : 'com_studentdashboard',
           'controller' : 'studentdashboard',
           'task' : 'dashboard'
          }
data = urllib.urlencode(values)
# getting the initial page
response = opener.open(url)
the_page = response.read()
