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


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','password']  # Add fields that can be edited

    password = forms.CharField(widget=forms.PasswordInput, required=False) 
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
            
        }

from django import forms
from .models import IrrigationZone
class StyledRadioSelect(forms.RadioSelect):
    template_name = "widgets/styled_radio.html"  # Create this template

class IrrigationZoneForm(forms.ModelForm):
    YES_NO_CHOICES = [(True, 'Yes'), (False, 'No')]
    zone_number = forms.IntegerField(required=True, label="Zone Number")  # Ensure it's required
    zone_faults = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Zone Faults?", required=False)
    checked_filters = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Checked Filters?", required=False)
    clogged_nozzles = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Clogged Nozzles?", required=False)
    head_adjusted = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Head Adjusted?", required=False)
    
    billable_repairs = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Billable Repairs?", required=False)
    spray_nozzle_repair = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Spray Nozzle Repair?", required=False)
    dripline_break = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Dripline Break?", required=False)
    severe_line_clog = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Severe Line Clog?", required=False)
    lateral_line_break = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Lateral Line Break?", required=False)
    relocation = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Relocation?", required=False)
    head_raised_lowered_turf = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Head Raised/Lowered - Turf?", required=False)
    head_raised_lowered_shrub = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Head Raised/Lowered - Shrub?", required=False)
    
    damaged_valve_box = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Damaged Valve Box?", required=False)
    valve_operating = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Valve Operating?", required=False)
    rain_sensor_operating = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Rain Sensor Operating?", required=False)
    controller_operating = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Controller Operating?", required=False)
    class Meta:
        model = IrrigationZone
        exclude = ['report']



class AccountManagerContactForm(forms.ModelForm):
    class Meta:
        model = AccountManagerContact
        exclude = ['report']  # 🚀 Exclude 'report' so it is auto-assigned in views

class IrrigationProgramForm(forms.ModelForm):
    class Meta:
        model = IrrigationProgram
        exclude = ['report']  # 🚀 Exclude 'report' so it is auto-assigned in views