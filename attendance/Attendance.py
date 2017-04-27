#!/usr/bin/env python
import sys

import lxml.html
import requests


def print_list_items(list):
    for i in range(len(list)):
        print i, list[i]


def get_attendance(lms_username, password, sem_i):

    # Loggin In
    s = requests.session()
    login_url = 'http://lms.bml.edu.in/login/index.php'
    dash_url = 'http://lms.bml.edu.in/local/dashboard/index.php'

    year = lms_username.split('.')[2][:2]

    print '-' * 103
    print 'Name : ' + lms_username.split('.')[0].title() + ' ' + lms_username.split('.')[1].title()
    print 'Year : ' + str(year)
    print 'Batch: ' + lms_username.split('.')[2][2:].upper()
    print 'Sem  : ', sem_i

    # Formatting sem variable to search for courses
    if year == '15':
        if sem_i == 1:
            sem = 'Sem I'
        elif sem_i == 2:
            sem = 'Sem II'
        elif sem_i == 3:
            sem = 'SEM III'
        elif sem_i == 4:
            sem = 'SEM IV'
        else:
            print 'Sem Preference not entered! Displaying All Sems!'
            sem = ''
    elif year == '16':
        if sem_i == 1:
            sem = 'SEM I'
        if sem_i == 2:
            sem = 'SEM II'
        else:
            print 'Sem Preference not entered! Displaying All Sems!'
            sem = ''

    login = s.get(login_url)
    login_html = lxml.html.fromstring(login.content)
    hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
    form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
    form['username'] = lms_username
    form['password'] = password
    response = s.post(login_url, data=form)

    print '-' * 103
    if response.url == dash_url:
        print 'Login Succees!'
    else:
        print 'Could Not Login! Check Details!'
        sys.exit()

    # Searching for attendance link
    res_html = lxml.html.fromstring(response.content)
    res_links = res_html.xpath('//a[@class="btn-block "]/@href')
    attendance_link = ''

    for i in range(len(res_links)):
        if 'http://lms.bml.edu.in/mod/attendance/myattendance.php?studentid' in res_links[i]:
            attendance_link = res_links[i]

    # Extracting info from Attendance Page
    attendance_page = s.get(attendance_link)
    attendance_html = lxml.html.fromstring(attendance_page.content)
    subjects = attendance_html.xpath('//a[@class="panel-title"]/text()')
    totalClasses = attendance_html.xpath(
        '//div[@class="attendance-report-wrapper"]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/text()')
    present = attendance_html.xpath('//div[@class="attendance-report-wrapper"]/div[2]/table[1]/tbody[1]/tr[1]/td['
                                    '2]/text()')
    absent = attendance_html.xpath('//div[@class="attendance-report-wrapper"]/div[2]/table[1]/tbody[1]/tr[1]/td['
                                   '3]/text()')
    attendace = {}
    sem_subjets = []

    # Formatting Subjects
    for i in range(len(subjects)):
        if sem in subjects[i]:
            sem_subjets += [i]
        temp = subjects[i].split(':')
        if len(temp) > 1:
            subjects[i] = temp[2].strip()[:-12]
        else:
            subjects[i] = temp[0].split('-')[0]

    # Printing Details
    print '-' * 103
    print '{0:50}||{1:5}|{2:7}|{3:6}|{4:7}|{5:6}|{6:6}| Set ah? '.format('Course', 'Total', 'Present', 'Absent', '   %',
                                                                         'For 80', 'For 75')
    print '-' * 103

    for i in range(len(sem_subjets)):
        k = sem_subjets[i]

        if totalClasses[k] != '0':
            perc = (float(present[k])) / float(totalClasses[k]) * 100
        else:
            perc = -1

        comment = ''
        if perc >= 80:
            comment = '{0:6}|{1:6}| SET!'.format('  SET', '  SET')
        elif perc == -1:
            perc = 0
            comment = '{0:6}|{1:6}| SET!'.format('  SET', '  SET')
        elif perc >= 75:
            classes80 = int(absent[k]) * 5 - int(totalClasses[k])
            comment = '{0:4d}  |{1:6}| uh?'.format(classes80, '  SET')
        else:
            classes80 = int(absent[k]) * 5 - int(totalClasses[k])
            classes75 = int(absent[k]) * 4 - int(totalClasses[k])
            comment = '{0:4d}  |{1:4d}  | Dhadel!'.format(classes80, classes75)

        print u'{0:50}||{1:4d} |{2:5d}  |{3:4d}  |{4:6.2f}%|{5:15}'.format(subjects[k], int(totalClasses[k]),
                                                                           int(present[k]), int(absent[k]), float(perc),
                                                                           comment)
    print '-' * 103

    # Loggin Out
    page_html = lxml.html.fromstring(response.content)
    logout = page_html.xpath(r'//a[@title = "Log out"]/@href')
    response = s.post(logout[0])
    if response.url == 'http://lms.bml.edu.in/':
        print 'Logout Success!'
    else:
        print 'Logout Faield!'
    print '-' * 103
    
