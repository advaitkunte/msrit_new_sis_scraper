#!/usr/bin/python

from bs4 import BeautifulSoup
import json

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

def details(row):
    subs = []
    for details in row[5].findAll('div',{'class':'big_container'}):
        data = {}
        t = details.findAll('td')
        attendance = t[9].findAll('span')
        try:
            data['attended'] = attendance[0].string.strip()
        except Exception as e:
            data['attended'] = 0
        try:
            data['conducted'] = attendance[1].string.strip()
        except Exception as e:
            data['conducted'] = 0
        data['code'] = t[0].string.strip()
        data['name'] = t[1].string.strip()
        data['attendance_percentage'] = t[7].string.strip()
        data['credits'] = t[14].string.strip()
        data['course_type'] = t[16].string.strip()
        data['course_nature'] = t[18].string.strip()
        data['cie_max_marks'] = t[20].string.strip()
        data['see_max_marks'] = t[22].string.strip()
        subs.append(data)

    return subs

def main():
    with open ("response.html", "r") as myfile:
        data=myfile.read()
    bs = BeautifulSoup(data)
    table = bs.find("td",{'width':'60%','style':'vertical-align:top;padding:0px 5px 0px 5px;border-right:1px dashed black'})
    row = table.findAll('tr')
    tt = timetable(row)
    det = details(row)
    final = {'timetable':tt, 'details':det}
    print json.dumps(final,indent = 4)