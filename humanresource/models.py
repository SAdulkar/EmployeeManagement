from django.db import models


class Hr(models.Model):
    name = models.CharField(max_length=90, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.TextField(default='password', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)



    