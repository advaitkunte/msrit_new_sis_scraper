#!/usr/bin/python

from bs4 import BeautifulSoup
import json
import time

# for today's timetable
def timetable(table):
    subs = []
    date = table.findAll('tr')[0].findAll('td')[0].findAll('td')[0].string.replace('Timetable','').strip()
    tt_subs = table.find('ul',{'id':'accordion1'}).findAll('li')
    if str(table.findAll('tr')[2]).find('No Classes Scheduled today!') > 0:
        data = {'subjects':subs,'date':date}
        return data
    for sub in tt_subs:
        sub = sub.find('div',{'class':'sliderslider'})
        data = {}
        data['time'] = sub.find('td',{'class':'left-top'}).string.strip()
        data['code'] = sub.find('td',{'class':'left-middle'}).string.strip()
        data['duration'] = sub.find('td',{'class':'left-bottom'}).string.strip()
        data['name'] = sub.find('div',{'class':'first'}).string.strip()
        x = sub.findAll('div',{'class':'right-bottom'})
        data['room'] = x[1].string.strip()
        data['semester'] = int(x[0].string.split('-')[0].replace('Semester','').strip())
        data['section'] = x[0].string.split('-')[1].replace('Section','').strip()
        subs.append(data)
    data = {'subjects':subs,'date':date}
    return data

def sis(table):
    subs = []
    for tab in table.findAll('div',{'class':'big_container'}):
        data = {}
        basic = tab.find('table').findAll('td')
        
        # basic
        data['sub_code'] = basic[0].string.strip()
        data['sub_name'] = basic[1].string.strip()
        
        # 
        attendance = tab.find('div',{'class':'boxmiddle'}).findAll('tr')
        marks = tab.find('div',{'class':'boxright'}).findAll('tr')
        details = tab.find('div',{'class':'boxleft'}).findAll('tr')
        
        # attendance
        data['percentage'] = attendance[2].string.strip()
        if attendance[4].findAll('span')[0].string:
            data['attended'] = int(attendance[4].findAll('span')[0].string)
        else:
            data['attended'] = 0
        
        if attendance[4].findAll('span')[1].string:
            data['conducted'] = int(attendance[4].findAll('span')[1].string)
        else:
            data['conducted'] = 0
        
        # details
        data['credits'] = details[4].string.strip()
        data['type'] = details[6].string.strip()
        data['nature'] = details[8].string.strip()
        data['cie_max'] = float("%0.2f" % float(details[10].string.strip()))
        data['see_max'] = float("%0.2f" % float(details[12].string.strip()))


        # CIE marks
        if len(marks) < 3:
            data['T1'] = float("%0.2f" % float(-1))
            data['T2'] = float("%0.2f" % float(-1))
            data['T3'] = float("%0.2f" % float(-1))
        else:
            # TODO 
            pass
        subs.append(data)
    return subs

def main(data):
    bs = BeautifulSoup(data,"lxml")
    table = bs.find("td",{'width':'60%','style':'vertical-align:top;padding:0px 5px 0px 5px;border-right:1px dashed black'})
    tt = timetable(table)
    det = sis(table)
    final = {'timetable':tt, 'details':det, 'status':200, 'desc':'success'}
    print json.dumps(final,indent = 4)

file = open('response-'+time.strftime("%d_%m_%Y")+'.html', 'r')
main(file.read())
