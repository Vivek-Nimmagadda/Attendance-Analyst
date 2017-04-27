from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=50)
    lmsId = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    last_updated = models.DateTimeField(blank=True, default=timezone.now)
    scholarship = models.BooleanField(default=True)

    def __str__(self):
        return self.name + ", " + self.lmsId


class Subjects(models.Model):
    name = models.CharField(max_length=50)
    sem = models.IntegerField(default=-1)


class Attendance(models.Model):
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_class = models.IntegerField(default=0)
    present_class = models.IntegerField(default=0)
    absent_class = models.IntegerField(default=0)
    for80 = models.IntegerField(default=0)
    for75 = models.IntegerField(default=0)


