
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class IrrigationReport(models.Model):
    technician = models.CharField(max_length=255)  # Will be prefilled but editable
    customer = models.CharField(max_length=100)  # Limit set to 100
    report_type = models.CharField(max_length=30)  # Limit set to 30
    controller_name = models.CharField(max_length=30)  # Limit set to 30
    date = models.DateField()  # We will enforce the date validation in the form
    programs_needed = models.BooleanField(default=False)
    
    weather_sensor_checked = models.BooleanField(default=False)
    weather_sensor_working = models.BooleanField(null=True, blank=True)
    
    controller_status = models.CharField(
        max_length=50, choices=[
            ('working', 'Working'),
            ('notWorking', 'Not Working'),
            ('notPresent', 'Not Present')
        ],
        blank=True, null=True
    )
    controller_make_model = models.CharField(max_length=30, blank=True, null=True)  # Limit set to 30
    
    poc_info = models.CharField(
        max_length=50, choices=[
            ('potable', 'Potable'),
            ('reclaimed', 'Reclaimed'),
            ('well', 'Well'),
            ('lake', 'Lake')
        ],
        blank=True, null=True
    )
    
    pump_status_type = models.CharField(
        max_length=50, choices=[
            ('pressurized', 'Pressurized'),
            ('reclaimed', 'Reclaimed'),
            ('pumpStart', 'Pump Start'),
            ('centrifugal', 'Centrifugal'),
            ('submersible', 'Submersible'),
            ('meterPoc', 'Meter POC')
        ]
    )

class IrrigationProgram(models.Model):
    report = models.ForeignKey(IrrigationReport, on_delete=models.CASCADE, related_name="programs", null=True, blank=True)
    program_name = models.CharField(max_length=30)  # Limit set to 30
    start_time = models.TimeField(null=True, blank=True)
    seasonal_adjustment = models.CharField(max_length=10, null=True, blank=True)
    run_days = models.JSONField(default=list)  # Stores selected run days as a JSON list

class IrrigationZone(models.Model):
    report = models.ForeignKey(IrrigationReport, on_delete=models.CASCADE, related_name="zones", null=True, blank=True)
    zone_number = models.IntegerField(null=True, blank=True)
    zone_type = models.CharField(max_length=50, choices=[
        ('Spray', 'Spray'), ('Rotor', 'Rotor'), ('MP', 'MP'), ('Drip', 'Drip'), ('Bubbler', 'Bubbler')
    ], null=True, blank=True)
    program_type = models.CharField(max_length=10, null=True, blank=True)
    run_time_schedule = models.CharField(max_length=255, blank=True, null=True)
    run_days = models.CharField(max_length=255, blank=True, null=True)
    
    power_type = models.CharField(max_length=50, choices=[('Battery', 'Battery'), ('Solar', 'Solar'), ('Hardwire', 'Hardwire')], blank=True, null=True)
    zone_faults = models.BooleanField(default=False, null=True, blank=True)
    zone_runtime = models.TimeField(default=None, null=True, blank=True)
    checked_filters = models.BooleanField(default=False, null=True, blank=True)
    clogged_nozzles = models.BooleanField(default=False, null=True, blank=True)
    head_adjusted = models.BooleanField(default=False, null=True, blank=True)
    
    billable_repairs = models.BooleanField(default=False, null=True, blank=True)
    head_broken_6 = models.IntegerField(default=0, null=True, blank=True)
    head_broken_12 = models.IntegerField(default=0, null=True, blank=True)
    broken_riser = models.IntegerField(default=0, null=True, blank=True)
    upgrade_4_popup = models.IntegerField(default=0, null=True, blank=True)
    upgrade_6_popup = models.IntegerField(default=0, null=True, blank=True)
    upgrade_12_popup = models.IntegerField(default=0, null=True, blank=True)
    upgrade_6_rotor = models.IntegerField(default=0, null=True, blank=True)
    upgrade_12_rotor = models.IntegerField(default=0, null=True, blank=True)
    nozzle_mpr = models.IntegerField(default=0, null=True, blank=True)
    nozzle_mp_rotator = models.IntegerField(default=0, null=True, blank=True)
    
    spray_nozzle_repair = models.BooleanField(default=False, null=True, blank=True)
    dripline_break = models.BooleanField(default=False, null=True, blank=True)
    severe_line_clog = models.BooleanField(default=False, null=True, blank=True)
    lateral_line_break = models.BooleanField(default=False, null=True, blank=True)
    relocation = models.BooleanField(default=False, null=True, blank=True)
    head_raised_lowered_turf = models.BooleanField(default=False, null=True, blank=True)
    head_raised_lowered_shrub = models.BooleanField(default=False, null=True, blank=True)
    
    damaged_valve_box = models.BooleanField(default=False, null=True, blank=True)
    valve_operating = models.BooleanField(default=False, null=True, blank=True)
    rain_sensor_operating = models.BooleanField(default=False, null=True, blank=True)
    controller_operating = models.BooleanField(default=False, null=True, blank=True)
    additional_labor = models.TextField(blank=True, null=True)

class AccountManagerContact(models.Model):
    report = models.ForeignKey(IrrigationReport, on_delete=models.CASCADE, related_name="account_manager_contact")
    contacted_manager = models.BooleanField(default=False)
    contact_time = models.TimeField(null=True, blank=True)
    communication_type = models.CharField(
        max_length=50, choices=[
            ('Spoke', 'Spoke'),
            ('Text', 'Text'),
            ('Voice Mail', 'Voice Mail')
        ],
        blank=True, null=True
    )
    additional_comments = models.TextField(blank=True, null=True)


class Branch(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the branch

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Name of the customer

    def __str__(self):
        return self.name  # Represent the customer by their name