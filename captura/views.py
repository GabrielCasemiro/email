# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import re
import urllib.request as urllib2


def home(request):
	return render(request, 'index.html', {})
def capturar(request):
	emails = []
	telefones = []

	if request.method == 'POST':
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
		link = request.POST.get("link", '')
		if link:
			req = urllib2.Request(link, headers=hdr)
			try:
				page = urllib2.urlopen(req)
			except urllib2.HTTPError:
				pass
			s = page.read().decode('utf-8')
			
			telefones = set(re.findall(r"\+\d{2}\s?0?\d{10}",s))
			emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s))
			msg = "Link Válido"
		return render(request, 'index.html', {"link":link,"msg":msg,"emails":emails,"telefones":telefones})
	return render(request, 'index.html')
