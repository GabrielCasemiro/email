# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import re
import urllib.request as urllib2
from captura.models import Counter, Report
from django.db.models import Count, F, Value

def home(request):
	contador = Counter.objects.get_or_create(pk = 0)
	return render(request, 'index.html', {"visitas":contador[0].visitas,"contador_emails":contador[0].emails,"contador_telefones":contador[0].telefones})
def capturar(request):
	emails = []
	telefones = []
	path = True
	contador = Counter.objects.get_or_create(pk = 0)
	msg = "Link Inválido. Não esqueça do http://"
	if request.method == 'POST':
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
		link = request.POST.get("link", '')
		if link:
			try:
				req = urllib2.Request(link, headers=hdr)
				page = urllib2.urlopen(req)
			except:
				return render(request, 'index.html', {"link":link,
				"msg":msg,
				"emails":emails,
				"telefones":telefones,
				"visitas":contador[0].visitas,
				"contador_emails":contador[0].emails,
				"contador_telefones":contador[0].telefones,
				"path":path
				})
			s = page.read().decode('utf-8')
			
			telefones = set(re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',s))
			emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}",s))
			if telefones or emails:
				report = Report.objects.create()
				report.emails = ''.join(str(e)+", " for e in emails)
				report.telefones = ''.join(str(e)+", " for e in telefones)
				report.url = link
				report.save()

				counter = Counter.objects.get_or_create(pk = 0)
				counter[0].emails = F('emails') + len(emails)
				counter[0].telefones = F('telefones') + len(telefones)
				counter[0].visitas = F('visitas') + 1
				counter[0].save(update_fields=["emails","telefones","visitas"])
			msg = u"Emails encontados: %s. Telefones encontrados: %s" % (len(emails),len(telefones))
		return render(request, 'index.html', {"link":link,
			"msg":msg,
			"emails":emails,
			"telefones":telefones,
			"visitas":contador[0].visitas,
			"contador_emails":contador[0].emails,
			"contador_telefones":contador[0].telefones,
			"path":path
			})
	else:
		return render(request, 'index.html', {"visitas":contador[0].visitas,
			"contador_emails":contador[0].emails,
			"path":path,
			"contador_telefones":contador[0].telefones})
		