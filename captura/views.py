# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import urllib,re
# Create your views here.
def home(request):
	return render(request, 'index.html', {})
def capturar(request):
	emails = []
	telefones = []

	if request.method == 'POST':
		link = request.POST.get("link", '')
		if link:
			f = urllib.urlopen(link)
			s = f.read()
			telefones = re.findall(r"\+\d{2}\s?0?\d{10}",s)
			emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s)
			msg = "Link Válido"
		return render(request, 'index.html', {"link":link,"msg":msg,"emails":emails,"telefones":telefones})
	return render(request, 'index.html')