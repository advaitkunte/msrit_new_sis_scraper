#!/usr/bin/python

from bs4 import BeautifulSoup
import json
import time

# for today's timetable
def timetable(row):
    date = row[1].string.replace('Timetable','').strip()
    subs = []
    if not str(row[2]).find('No Classes Scheduled today!') > 0:
        for timetable in row[2].findAll('li'):
            data = {}
            data['name'] = timetable.find('div',{'class':'first'}).string.strip()
            x = timetable.find('div',{'class':'second'}).findAll('div',{'class':'right-bottom'})
            data['room'] = x[1].string.strip()
            xx = timetable.find('div',{'class':'left'}).findAll('td')
            data['time'] = xx[0].string
            data['code'] = xx[1].string
            data['duration'] = xx[2].string
            xy = x[0].string.strip().split('-')
            data['semester'] = xy[0].replace('Semester','').strip()
            data['section'] = xy[1].replace('Section','').strip()
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
    bs = BeautifulSoup(data)
    table = bs.find("td",{'width':'60%','style':'vertical-align:top;padding:0px 5px 0px 5px;border-right:1px dashed black'})
    # table = bs.find('div',{'id':'left-column'}).find('table',{'width':'980px'}).findAll('tr')[2].find('td',{'style':'vertical-align:top;padding:0px 5px 0px 5px;border-right:1px dashed black'})

    tt = timetable(table.findAll('tr'))
    det = sis(table)
    final = {'timetable':tt, 'sis':det, 'status':200, 'desc':'success'}
    
    print json.dumps(final,indent = 4)

file = open('response-'+time.strftime("%d_%m_%Y")+'.html', 'r')
main(file.read())