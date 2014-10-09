#!/usr/bin/python

import random
import math
import urllib
import urllib2
from bs4 import BeautifulSoup
import base64,cookielib
# import get_data
import json
import time

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

username = ""
password = ""

url = 'http://parents.msrit.edu/index.php'
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36'
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

try:
    # to get first cookie and other parameters
    response = opener.open(url)

    token = []
    val = ''
    bs = BeautifulSoup(response.read())
    table = bs.find("table").find('tr').findAll('input')

    val = table[len(table)-3].get('value')
    token.append(table[len(table)-1].get('name'))
    token.append(table[len(table)-1].get('value'))

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
    the_page = response.read()

    if url == 'http://parents.msrit.edu/index.php':
        data = {'status':1,'desc':'Invalid Username / Password'}
        print json.dumps(data,indent = 4)
    else:
        filename = 'response-'+time.strftime("%d_%m_%Y")+'.html'
        f = open(filename, 'w')
        f.write(the_page)
        f.close()
        data = {'status':200, 'desc':'success'}
        print json.dumps(data,indent = 4)
except Exception as e:
    data = {'status':500, 'desc':str(e.reason)}
    print json.dumps(data,indent = 4)
