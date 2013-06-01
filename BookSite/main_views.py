# -*- coding: utf8 -*-
from django.http import HttpResponse

#for template
from django.template import Context, loader

def main_page(req):
	return HttpResponse("Text only, please.")