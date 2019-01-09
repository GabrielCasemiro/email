# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Report, Counter

admin.site.register(Report)
admin.site.register(Counter)
# Register your models here.
