from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request

from models import Student, Subjects, Attendance
from attendance.encryption import encode, decode
from django.utils import timezone
import lxml.html
import requests
from .forms import RegisterForm, EditProfile
import json

# Create your views here.


def index(request):
    student_list = Student.objects.all().order_by('last_updated').reverse()
    time_now = timezone.now()
    return render(request, 'attendance/index.html', {'studentList': student_list, 'currentTime': time_now})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        print request.POST
        if form.is_valid():
            new_student = Student(name=form.cleaned_data['user_name'], lmsId=form.cleaned_data['lms_id'],
                                  password=encode(form.cleaned_data['password']))
            new_student.display_image = form.cleaned_data['profile_picture']

            new_student.save()

            return HttpResponse(new_student.name + "'s Registration Success!")

    else:
        form = RegisterForm()

    return render(request, 'attendance/register.html', {'form': form, 'navRegisterClass': 'active'})


def edit(request, lms_id):
    temp = Student.objects.get(lmsId=lms_id)
    form = EditProfile()
    return render(request, 'attendance/editProfile.html', {'student': temp, 'form': form})


def about(request):
    return render(request, 'attendance/about.html', {'navAboutClass':'active'})


def update_records(request, lms_id):
    if request.method == 'POST':
        student = Student.objects.get(lmsId=lms_id)

        status = ""

        # Logging In
        s = requests.session()
        login_url = 'http://lms.bml.edu.in/login/index.php'
        dash_url = 'http://lms.bml.edu.in/local/dashboard/index.php'

        year = student.lmsId.split('.')[2][:2]

        print '-' * 103
        print 'Name : ' + student.lmsId.split('.')[0].title() + ' ' + student.lmsId.split('.')[1].title()
        print 'Year : ' + str(year)
        print 'Batch: ' + student.lmsId.split('.')[2][2:].upper()

        sem = 'Sem I'

        login = s.get(login_url)
        login_html = lxml.html.fromstring(login.content)
        hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
        form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}
        form['username'] = student.lmsId
        form['password'] = decode(student.password)
        response = s.post(login_url, data=form)

        print '-' * 103
        if response.url == dash_url:
            status = "Login Succees!"
            print status
        else:
            status = 'Could Not Login! Check Details!'
            print status
            return render(request, "attendance/error.html", {})

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
        total_classes = attendance_html.xpath(
            '//div[@class="attendance-report-wrapper"]/div[2]/table[1]/tbody[1]/tr[1]/td[1]/text()')
        present = attendance_html.xpath('//div[@class="attendance-report-wrapper"]/div[2]/table[1]/tbody[1]/tr[1]/td['
                                        '2]/text()')
        absent = attendance_html.xpath('//div[@class="attendance-report-wrapper"]/div[2]/table[1]/tbody[1]/tr[1]/td['
                                       '3]/text()')

        sem_subjects = []

        sub_array = []
        # Formatting Subjects
        for i in range(len(subjects)):
            sem_subjects += [i]
            temp = subjects[i].split(':')
            num = -1
            if "SEM IV" in subjects[i]:
                num = 4
            elif "SEM III" in subjects[i]:
                num = 3
            elif "SEM II" in subjects[i]:
                num = 2
            elif "Sem II" in subjects[i]:
                num = 2
            elif "SEM I" in subjects[i]:
                num = 1
            elif "Sem I" in subjects[i]:
                num = 1
            if len(temp) > 1:
                subjects[i] = temp[2].strip()[:-12]
            else:
                subjects[i] = temp[0].split('-')[0]
            sub_array.append({'name': subjects[i], 'sem': num})

        k = 0
        subjects_array = []
        for subject in sub_array:
            try:
                test = Subjects.objects.get(name=subject)
            except Exception:
                test = Subjects(name=subject['name'], sem=subject['sem'])
                test.save()
                pass
            k+=1
            subjects_array.append(test)

        # Printing Details
        print '-' * 103
        print '{0:50}||{1:5}|{2:7}|{3:6}|{4:7}|{5:6}|{6:6}| Set ah? '.format('Course', 'Total', 'Present', 'Absent', '   %',
                                                                             'For 80', 'For 75')
        print '-' * 103

        for i in range(len(sem_subjects)):
            k = sem_subjects[i]

            if total_classes[k] != '0':
                perc = (float(present[k])) / float(total_classes[k]) * 100
            else:
                perc = -1

            comment = ''
            if perc >= 80:
                comment = '{0:6}|{1:6}| SET!'.format('  SET', '  SET')
            elif perc == -1:
                perc = 0
                comment = '{0:6}|{1:6}| SET!'.format('  SET', '  SET')
            elif perc >= 75:
                classes80 = int(absent[k]) * 5 - int(total_classes[k])
                comment = '{0:4d}  |{1:6}| uh?'.format(classes80, '  SET')
            else:
                classes80 = int(absent[k]) * 5 - int(total_classes[k])
                classes75 = int(absent[k]) * 4 - int(total_classes[k])
                comment = '{0:4d}  |{1:4d}  | Dhadel!'.format(classes80, classes75)

            print u'{0:50}||{1:4d} |{2:5d}  |{3:4d}  |{4:6.2f}%|{5:15}'.format(subjects[k], int(total_classes[k]),
                                                                               int(present[k]), int(absent[k]),
                                                                               float(perc),comment)

            try:
                temp = Attendance.objects.filter(student__lmsId=student.lmsId).get(subject__name=subjects[k])
                # print temp
                temp.present_class = present[k]
                temp.absent_class = absent[k]
                temp.total_class = total_classes[k]
                temp.for75 = int(absent[k]) * 4 - int(total_classes[k])
                temp.for80 = int(absent[k]) * 5 - int(total_classes[k])
                temp.save()
            except Exception:
                temp = Attendance(student=student, subject=subjects_array[k],
                                  present_class=present[k], absent_class=absent[k], total_class=total_classes[k],
                                  for75=int(absent[k])*4 - int(total_classes[k]), for80=int(absent[k])*5 - int(total_classes[k]))
                temp.save()

        print '-' * 103
        student.last_updated = timezone.now()
        student.save()
        print student.last_updated
        # Loggin Out
        page_html = lxml.html.fromstring(response.content)
        logout = page_html.xpath(r'//a[@title = "Log out"]/@href')
        response = s.post(logout[0])
        if response.url == 'http://lms.bml.edu.in/':
            status = 'Logout Success!'
            print status
        else:
            status = 'Logout Failed!'
            print status
        print '-' * 103
        return redirect('/attendance/' + student.lmsId + "/" + "4" + "/#focus")
    return HttpResponse("Failure!")


def get_records(request, lms_id, sem):
    attendance_query = Attendance.objects.filter(student__lmsId=lms_id, subject__sem=int(sem))

    table_list = []
    percet_list = []
    sub_list = []
    list_80 = []
    list_75 = []
    for attendance_record in attendance_query:
        if attendance_record.total_class != 0:
            perc = 100 - (float(attendance_record.absent_class)) / float(attendance_record.total_class) * 100
        else:
            perc = -1

        if perc >= 80:
            classes75 = "SET"
            classes80 = "SET"
            comment = "SET"
        elif perc == -1:
            perc = 0
            classes75 = "SET"
            classes80 = "SET"
            comment = "SET"
        elif perc >= 75:
            classes80 = int(attendance_record.absent_class) * 5 - int(attendance_record.total_class)
            comment = "uh?"
            if classes80 >= 0 :
                classes80 = classes80
            else:
                classes80 = "SET!"
            classes75 = "SET!"
        else:
            classes80 = int(attendance_record.absent_class) * 5 - int(attendance_record.total_class)
            classes75 = int(attendance_record.absent_class) * 4 - int(attendance_record.total_class)
            comment = "Dhadel!"
            if classes80 >= 0:
                classes80 = classes80
            else:
                classes80 = "SET!"
            if classes75 >= 0:
                classes75 = classes75
            else:
                classes80 = "SET!"
        table_list_item = {'name': attendance_record.subject.name, 'total': attendance_record.total_class, 'present': attendance_record.present_class,
                           'absent': attendance_record.absent_class, 'perc': perc, 'comment': comment, 'for80': classes80, 'for75': classes75}
        table_list.append(table_list_item)
        perc = "%.2f" % perc
        percet_list.append(perc)
        sub_list.append(attendance_record.subject.name)
        if type(classes80) == int:
            list_80.append(classes80)
        else:
            list_80.append(0)
        if type(classes75) == int:
            list_75.append(classes75)
        else:
            list_75.append(0)

    student_retrieved = Student.objects.get(lmsId=lms_id)
    sem_list = list_of_sems(student_retrieved)
    sub_list = json.dumps(sub_list)
    context = {'student_retrieved': student_retrieved, 'table_list': table_list,
               'currentTime': timezone.now(), 'semList': sem_list, 'cur_sem': int(sem),
               'percList': percet_list, 'subList': sub_list, 'list80': list_80, 'list75': list_75}

    # print percet_list
    return render(request, 'attendance/result.html', context)


def list_of_sems(student):
    sem_query = Attendance.objects.filter(student_id=student.id)
    sem_list = []

    for attendance in sem_query:
        if attendance.subject.sem in sem_list:
            continue
        else:
            sem_list.append(attendance.subject.sem)

    sem_list.sort()
    return sem_list
