# Generated by Django 5.1.6 on 2025-03-18 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_irrigationzone_program_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='irrigationzone',
            name='zone_runtime',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='irrigationzone',
            name='zone_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
