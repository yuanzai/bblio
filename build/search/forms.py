from django import forms
from django.forms.formsets import BaseFormSet
from models import TestingResult
#class TestingFormSet(BaseFormSet):
#    def add(self, form)
        

class TestingForm(forms.ModelForm):
    class Meta:
        model = TestingResult
        fields = ['document', 'score', 'testinggroup', 'searchterm']

class AdminURLListForm(forms.Form):
    source_denyParse = forms.CharField(required=False,widget=forms.TextInput(attrs={'size': '120'}))

class TestingFormResult(forms.Form):
    document = forms.IntegerField(widget=forms.HiddenInput())
    score = forms.IntegerField(required=False,widget=forms.TextInput(attrs={'size': '4'}))

class TestingFormPage(forms.Form):
    testinggroup = forms.IntegerField()
    searchterm = forms.CharField()
