from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Customer, IrrigationReport, IrrigationProgram, IrrigationZone, AccountManagerContact, Branch, UserBranch
from datetime import datetime
from django.forms.widgets import TimeInput

# Sign-up form
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    branch = forms.ModelChoiceField(queryset=Branch.objects.all(), empty_label="Select Branch")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'branch']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','password']  # Add fields that can be edited

    password = forms.CharField(widget=forms.PasswordInput, required=False) 
# Sign-in form
class SigninForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)




from datetime import date  # <-- Add this import
from django_select2.forms import ModelSelect2Widget

class IrrigationReportForm(forms.ModelForm):
    technician = forms.CharField(
        label='Technician',
        widget=forms.TextInput(attrs={
            'class': 'w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-200'
        })
    )
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=forms.Select(attrs={
            'class': 'select2 w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-200'
        }),

    )
    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all(),
        widget=forms.Select(attrs={
            'class': 'select2 w-full p-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-200'
        }),
        empty_label="Select Branch"
    )
    
    class Meta:
        model = IrrigationReport
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'max': date.today().strftime('%Y-%m-%d')
            }),
            'customer': forms.TextInput(attrs={'maxlength': '100'}),
            'report_type': forms.TextInput(attrs={'maxlength': '30'}),
            'controller_name': forms.TextInput(attrs={'maxlength': '30'}),
            'controller_make_model': forms.TextInput(attrs={'maxlength': '30'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            self.fields['technician'].initial = user.username
            
            # Fetch the branch associated with the user
            try:
                user_branch = UserBranch.objects.get(user=user)
                self.fields['branch'].initial = user_branch.branch  # Set the branch field to the user's branch
            except UserBranch.DoesNotExist:
                self.fields['branch'].initial = None  # If no branch is found, leave it empty

        # Set the default value of 'date' to today
        self.fields['date'].initial = date.today().strftime('%Y-%m-%d')

    def clean_controller_make_model(self):
        """Ensure controller_make_model is required if controller_status is 'working'"""
        status = self.cleaned_data.get('controller_status')
        make_model = self.cleaned_data.get('controller_make_model')

        if status == 'working' and not make_model:
            raise forms.ValidationError("Controller Make/Model is required when status is 'Working'.")
        return make_model


class IrrigationProgramForm(forms.ModelForm):
    class Meta:
        model = IrrigationProgram
        fields = '__all__'
        exclude = ['report']
        widgets = {
            'program_name': forms.TextInput(attrs={'maxlength': '30'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_program_name(self):
        """Ensure program name is mandatory"""
        program_name = self.cleaned_data.get('program_name')
        if not program_name:
            raise forms.ValidationError("Program Name is required.")
        return program_name

    def clean_start_time(self):
        """Ensure start time is mandatory"""
        start_time = self.cleaned_data.get('start_time')
        if not start_time:
            raise forms.ValidationError("Start Time is required.")
        return start_time

    def clean_run_days(self):
        """Ensure at least one run day is selected"""
        run_days = self.cleaned_data.get('run_days')
        if not run_days:
            raise forms.ValidationError("At least one run day must be selected.")
        return run_days


from django import forms
from .models import IrrigationZone
import string

class StyledRadioSelect(forms.RadioSelect):
    template_name = "widgets/styled_radio.html"  # Create this template

class IrrigationZoneForm(forms.ModelForm):
    YES_NO_CHOICES = [(True, 'Yes'), (False, 'No')]
    
    zone_number = forms.IntegerField(required=False,  label="Zone Number")  # Ensure it's required
    zone_faults = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Zone Faults?", required=False, initial=False)
    zone_runtime = forms.TimeField(
        widget=TimeInput(attrs={
            'type': 'time',
            'class': 'w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
            'placeholder': 'Select Time'
        }),
        label="Zone Run Time",
        required=False,
        initial=None
    )
    checked_filters = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Checked Filters?", required=False, initial=True)
    clogged_nozzles = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Clogged Nozzles?", required=False, initial=False)
    head_adjusted = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Head Adjusted?", required=False, initial=False)
    
    billable_repairs = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Billable Repairs?", required=False)
    spray_nozzle_repair = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Spray Nozzle Repair?", required=False, initial=False)
    dripline_break = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Dripline Break?", required=False, initial=False)
    severe_line_clog = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Severe Line Clog?", required=False, initial=False)
    lateral_line_break = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Lateral Line Break?", required=False, initial=False)
    relocation = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Relocation?", required=False, initial=False)
    head_raised_lowered_turf = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Head Raised/Lowered - Turf?", required=False, initial=False)
    head_raised_lowered_shrub = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Head Raised/Lowered - Shrub?", required=False, initial=False)
    
    damaged_valve_box = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Damaged Valve Box?", required=False, initial=False)
    valve_operating = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Valve Operating?", required=False, initial=False)
    rain_sensor_operating = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Rain Sensor Operating?", required=False, initial=False)
    controller_operating = forms.ChoiceField(choices=YES_NO_CHOICES, widget=StyledRadioSelect(), label="Controller Operating?", required=False, initial=False)

    program_type = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'w-full p-2 border rounded-md'}), required=False,  label="Program Type" )

    class Meta:
        model = IrrigationZone
        exclude = ['report']

    def __init__(self, *args, **kwargs):
        report = kwargs.pop('report', None)
        super().__init__(*args, **kwargs)
        self.fields['program_type'].choices = [('', 'Select a Program')] + self.get_program_type_choices(report)


    def get_program_type_choices(self, report):
        """Generates dynamic choices based on the number of programs for the report."""
        base_choices = [('House', 'House')]
        print(report)
        if report:
            program_count = IrrigationProgram.objects.filter(report=report).count()
            program_choices = [(letter, letter) for letter in string.ascii_uppercase[:program_count]]
            print(program_choices)
            print(program_count)
            print(program_choices + base_choices)
            return program_choices + base_choices
        return base_choices

class AccountManagerContactForm(forms.ModelForm):
    class Meta:
        model = AccountManagerContact
        exclude = ['report']  # 🚀 Exclude 'report' so it is auto-assigned in views

