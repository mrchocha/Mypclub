# Generated by Django 3.0.6 on 2020-06-24 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0022_user_user_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource_name', models.CharField(max_length=50)),
                ('resource_content', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Resource_Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(upload_to='resource_files/')),
                ('resource', models.ManyToManyField(to='app1.Resources')),
            ],
        ),
        migrations.CreateModel(
            name='Lable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tag', models.CharField(max_length=50)),
                ('resource', models.ManyToManyField(to='app1.Resources')),
            ],
        ),
    ]
