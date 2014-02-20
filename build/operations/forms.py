from django import forms
from django.forms.formsets import BaseFormSet
from django.forms import Textarea, TextInput
from search.models import TestingResult,Site
#class TestingFormSet(BaseFormSet):
#    def add(self, form)
        

class TestingForm(forms.ModelForm):
    class Meta:
        model = TestingResult
        fields = ['document', 'score', 'testinggroup', 'searchterm']

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = [
                'name','grouping','depthlimit',
                'source_allowed_domains',
                'source_start_urls',
                'source_allowParse',
                'source_denyParse',
                'source_allowFollow',
                'source_denyFollow']
        widgets = {
                'name': TextInput(attrs={'class': 'form-control'}),
                'grouping': TextInput(attrs={'class': 'form-control'}),
                'depthlimit': TextInput(attrs={'class': 'form-control'}),


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
                }

class AdminURLListForm(forms.Form):
    source_denyParse = forms.CharField(required=False,widget=forms.TextInput(attrs={'size': '120'}))

class TestingFormResult(forms.Form):
    document = forms.IntegerField(widget=forms.HiddenInput())
    score = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'size': '4'}))

class TestingFormPage(forms.Form):
    testinggroup = forms.IntegerField()
    searchterm = forms.CharField()
