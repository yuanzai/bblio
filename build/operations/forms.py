from django import forms
from django.forms.formsets import BaseFormSet
from django.forms import Textarea, TextInput, Select
from search.models import TestingResult,Site
from aws.ec2 import getCrawlerInstances
import config_file
from scraper.scrapeController import get_job_status_count_for_instance
        

class TestingForm(forms.ModelForm):
    class Meta:
        model = TestingResult
        fields = ['document', 'score', 'testinggroup', 'searchterm']

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        instance_list = []
        running_limit = config_file.get_config().get('bblio','crawler_instance_site_limit')
        for i in getCrawlerInstances():            
            dict = get_job_status_count_for_instance(i.id)
            count = int(dict['pending']) + int(dict['running'])
            instance_list.append({'name':i.id,'choice_name': i.id + ' ' + str(count) + '/' + str(running_limit)})

        instance_list.append({'name':'','choice_name':''})

        instance_choices = ((i['name'],i['choice_name']) for i in instance_list)
        fields = [
                'name','grouping','depthlimit','jurisdiction',
                'source_allowed_domains',
                'source_start_urls',
                'source_allowParse',
                'source_denyParse',
                'source_allowFollow',
                'source_denyFollow',
                'parse_parameters',
                'follow_parameters',
                'deny_parameters',
                'instance',
                ]
        widgets = {
                'name': TextInput(attrs={'class': 'form-control'}),
                'grouping': TextInput(attrs={'class': 'form-control'}),
                'depthlimit': TextInput(attrs={'class': 'form-control'}),

                'jurisdiction': TextInput(attrs={'class': 'form-control'}),

                'source_allowed_domains': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'source_start_urls': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'source_allowParse': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'source_denyParse': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'source_allowFollow': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'source_denyFollow': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'parse_parameters': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'follow_parameters': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'deny_parameters': Textarea(
                    attrs={'cols': 80, 'rows': 2, 'class': 'form-control'}),
                'instance': Select(attrs={'class': 'form-control'}, choices=instance_choices),
                }


class AdminURLListForm(forms.Form):
    source_denyParse = forms.CharField(required=False,widget=forms.TextInput(attrs={'size': '120'}))

class TestingFormResult(forms.Form):
    document = forms.IntegerField(widget=forms.HiddenInput())
    score = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'size': '4'}))

class TestingFormPage(forms.Form):
    testinggroup = forms.IntegerField()
    searchterm = forms.CharField()
