# Generated by Django 3.0.6 on 2020-06-25 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_lable_resource_files_resources'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_start_date',
            field=models.DateTimeField(),
        ),
    ]
