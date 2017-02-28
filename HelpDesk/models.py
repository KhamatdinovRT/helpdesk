from __future__ import unicode_literals
from django.db import models


class Request(models.Model):
    number = models.AutoField(primary_key=True)
    client = models.CharField(max_length=38)
    structure = models.ForeignKey('Structure', models.DO_NOTHING, db_column='structure', blank=True, null=True)
    office = models.CharField(max_length=38, blank=True, null=True)
    phone_number = models.CharField(max_length=38, blank=True, null=True)
    chief = models.ForeignKey('Users',  models.DO_NOTHING, related_name="chief_n", db_column='chief', blank=True, null=True)
    worker = models.ForeignKey('Users', models.DO_NOTHING, related_name="worker_n", db_column='worker', blank=True, null=True)
    receipt = models.DateField(blank=True, null=True)
    complete = models.DateField(blank=True, null=True)
    call = models.CharField(max_length=20, blank=True, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)
    report = models.CharField(max_length=200, blank=True, null=True)
    task_other = models.CharField(max_length=200, blank=True, null=True)
    request_status = models.ForeignKey('RequestStatus', models.DO_NOTHING, db_column='request_status', blank=True, null=True)
    tasks = models.ManyToManyField('TaskList')
    class Meta:
        managed = True
        db_table = 'request'
    
    def __str__(self):
        return "Заявка №" + str(self.number)
        
class RequestTasks(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    tasklist = models.ForeignKey('TaskList', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'request_tasks'
        unique_together = (('request', 'tasklist'),)

class RequestStatus(models.Model):
    id_status = models.AutoField(primary_key=True)
    name = models.CharField(max_length=38)

    class Meta:
        managed = False
        db_table = 'request_status'
    
    def __str__(self):
        return self.name

class Structure(models.Model):
    id_str = models.AutoField(primary_key=True)
    name = models.CharField(max_length=38)

    class Meta:
        managed = False
        db_table = 'structure'
    def __str__(self):
        return self.name


class TaskList(models.Model):
    id_task = models.AutoField(primary_key=True)
    name = models.CharField(max_length=38)

    class Meta:
        managed = True
        db_table = 'task_list'
    def __str__(self):
        return self.name


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=38)
    login = models.CharField(max_length=15)
    password = models.CharField(max_length=8)
    supervisor = models.BooleanField()
    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'users'

