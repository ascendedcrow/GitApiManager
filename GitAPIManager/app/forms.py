"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User Name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class createissueform(forms.Form):
    from GitAPIManager.GitApiFunctions import GetClientDropDown,GetCategoryDropDown,GetPriorityDropDown,GetUserDropDown

    title = forms.CharField(max_length=255,                               
                            widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Title'}))
    description = forms.CharField(max_length=255,                               
                            widget=forms.Textarea({
                                   'class': 'form-control',
                                   'placeholder': 'Description'}))
    client = forms.ChoiceField(choices = GetClientDropDown(None),required= True,
                               widget=forms.Select(attrs={'class':'form-control'}))
    priority = forms.ChoiceField(choices = GetPriorityDropDown(None),required= True,
                                 widget=forms.Select(attrs={'class':'form-control'}))
    category = forms.ChoiceField(choices = GetCategoryDropDown(None),required= True,
                                 widget=forms.Select(attrs={'class':'form-control'}))
    assignto = forms.ChoiceField(choices = GetUserDropDown(None),required= True,
                                 widget=forms.Select(attrs={'class':'form-control'}))