from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=90, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.TextField(default='password', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    hired_date = models.DateField(null=True, blank=True)

class EmployeeSalary(models.Model):
    email = models.EmailField()
    date = models.DateField(auto_now_add=True)
    salary = models.CharField(max_length=20)

class RemainLeave(models.Model):
    email = models.EmailField()
    total_leave = models.IntegerField(default=0)

class LeaveRequest(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    leave_date_from = models.DateField()
    leave_date_to = models.DateField()
    reason = models.TextField()
    leave_status = models.CharField(max_length=10,default=None,blank=True,null=True)


class Notifications(models.Model):
    title = models.CharField(max_length=60)
    message  = models.TextField()