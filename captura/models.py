# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Counter(models.Model):
    visitas = models.IntegerField(default=1)
    telefones = models.IntegerField(default=1)
    emails = models.IntegerField(default=1)

class Report(models.Model):
    emails = models.CharField(max_length=15000,default='')
    telefones = models.CharField(max_length=15000,default='')
    url = models.CharField(max_length=15000,default='')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url