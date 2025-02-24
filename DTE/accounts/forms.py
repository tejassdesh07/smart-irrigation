from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import IrrigationReport, IrrigationProgram, IrrigationZone, AccountManagerContact

# Sign-up form
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

# Sign-in form
class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class IrrigationReportForm(forms.ModelForm):
    class Meta:
        model = IrrigationReport
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'report_type': forms.Select(choices=[('Monthly', 'Monthly'), ('Annual', 'Annual')]),
        }

class IrrigationZoneForm(forms.ModelForm):
    class Meta:
        model = IrrigationZone
        exclude = ['report']  # 🚀 Exclude 'report' so it is auto-assigned in views

class AccountManagerContactForm(forms.ModelForm):
    class Meta:
        model = AccountManagerContact
        exclude = ['report']  # 🚀 Exclude 'report' so it is auto-assigned in views

class IrrigationProgramForm(forms.ModelForm):
    class Meta:
        model = IrrigationProgram
        exclude = ['report']  # 🚀 Exclude 'report' so it is auto-assigned in views