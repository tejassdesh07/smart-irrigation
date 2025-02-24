from django.db import models


class IrrigationReport(models.Model):
    technician = models.CharField(max_length=255)
    customer = models.CharField(max_length=255)
    report_type = models.CharField(max_length=255)
    controller_name = models.CharField(max_length=255)
    date = models.DateField()
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
    controller_make_model = models.CharField(max_length=255, blank=True, null=True)
    
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
            ('pumpStart', 'Pump Start'),
            ('centrifugal', 'Centrifugal'),
            ('submersible', 'Submersible')
        ]
    )
class IrrigationProgram(models.Model):
    report = models.ForeignKey(IrrigationReport, on_delete=models.CASCADE, related_name="programs", null=True, blank=True)
    program_name = models.CharField(max_length=10)
    start_time = models.TimeField(null=True, blank=True)
    seasonal_adjustment = models.CharField(max_length=10, null=True, blank=True)
    run_days = models.JSONField(default=list)

class IrrigationZone(models.Model):
    report = models.ForeignKey(IrrigationReport, on_delete=models.CASCADE, related_name="zones")
    zone_number = models.IntegerField()
    zone_type = models.CharField(max_length=50, choices=[
        ('Spray', 'Spray'), ('Rotor', 'Rotor'), ('MP', 'MP'), ('Drip', 'Drip'), ('Bubbler', 'Bubbler')
    ])
    program_type = models.CharField(max_length=10, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('House', 'House')])
    run_time_schedule = models.CharField(max_length=255, blank=True, null=True)
    run_days = models.CharField(max_length=255, blank=True, null=True)
    
    power_type = models.CharField(max_length=50, choices=[('Battery', 'Battery'), ('Doubler', 'Doubler')], blank=True, null=True)
    zone_faults = models.BooleanField(default=False)
    checked_filters = models.BooleanField(default=False)
    clogged_nozzles = models.BooleanField(default=False)
    head_adjusted = models.BooleanField(default=False)
    
    billable_repairs = models.BooleanField(default=False)
    head_broken_6 = models.IntegerField(default=0)
    head_broken_12 = models.IntegerField(default=0)
    broken_riser = models.IntegerField(default=0)
    upgrade_46_popup = models.IntegerField(default=0)
    upgrade_612_popup = models.IntegerField(default=0)
    nozzle_mpr = models.IntegerField(default=0)
    nozzle_mp_rotator = models.IntegerField(default=0)
    
    spray_nozzle_repair = models.BooleanField(default=False)
    dripline_break = models.BooleanField(default=False)
    severe_line_clog = models.BooleanField(default=False)
    lateral_line_break = models.BooleanField(default=False)
    relocation = models.BooleanField(default=False)
    head_raised_lowered_turf = models.BooleanField(default=False)
    head_raised_lowered_shrub = models.BooleanField(default=False)
    
    damaged_valve_box = models.BooleanField(default=False)
    valve_operating = models.BooleanField(default=False)
    rain_sensor_operating = models.BooleanField(default=False)
    controller_operating = models.BooleanField(default=False)
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
