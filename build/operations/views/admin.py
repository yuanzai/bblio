#python imports
import re
import urllib
import cgi
import sys

#django app imports
from build.search.models import Document, Site, TestingResult, TestingGroup, Phrase
from build.operations.forms import TestingFormPage, TestingFormResult, AdminURLListForm, SiteForm

#django imports
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, modelform_factory
from django.core.urlresolvers import reverse
from django import forms
from django.forms.models import model_to_dict

#es import
from es.YTHESController import YTHESController as ESController

#crawler import
import scraper.scrapeController
import scraper.linkextract

#distributed import
import aws.scrapeMaster


def index(request):
    return HttpResponse('Place Holder Page')

      
