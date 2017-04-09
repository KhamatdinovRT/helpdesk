from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.timezone import now

class Request(models.Model):
    number = models.AutoField(primary_key=True)
    client = models.CharField(max_length=38)
    structure = models.ForeignKey('Structure', models.DO_NOTHING, db_column='structure', blank=False, null=True)
    office = models.CharField(max_length=38, blank=False)
    phone_number = models.CharField(max_length=38, blank=False, null=False)
    chief = models.ForeignKey('Users',  models.DO_NOTHING, related_name="chief_n", db_column='chief', blank=False, null=True)
    worker = models.ForeignKey('Users', models.DO_NOTHING, related_name="worker_n", db_column='worker', blank=False, null=True)
    receipt = models.DateField(blank=False, null=True, default=now)
    complete = models.DateField(blank=True, null=True)
    comments = models.CharField(max_length=100, blank=True)
    report = models.CharField(max_length=100, blank=True, null=True)
    task_other = models.CharField(max_length=100, blank=True)
    request_status = models.ForeignKey('RequestStatus', models.DO_NOTHING, db_column='request_status', blank=False, default=3, null=True)
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
        managed = True
        db_table = 'request_status'
    
    def __str__(self):
        return self.name

class Structure(models.Model):
    id_str = models.AutoField(primary_key=True)
    name = models.CharField(max_length=38)

    class Meta:
        managed = True
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


class Users(AbstractUser):
    supervisor = models.BooleanField()
    def __str__(self):
        return self.first_name + ' ' + self.last_name   

    class Meta:
        managed = True
        db_table = 'users'

class TempRequest (models.Model):
    number = models.AutoField(primary_key=True)
    client = models.CharField(max_length=38)
    structure = models.CharField(max_length=38, blank=False, null=True)
    office = models.CharField(max_length=38, blank=False)
    phone_number = models.CharField(max_length=38, blank=False, null=False)
    receipt = models.DateField(blank=False, null=True, default=now)
    tasks = models.CharField(max_length=38, blank=False, null=False)
    comments = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = True
        db_table = 'temp_request'
    def __str__(self):
        return "Заявка №" + str(self.number)