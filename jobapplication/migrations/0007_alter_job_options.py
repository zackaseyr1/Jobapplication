# Generated by Django 4.2.1 on 2023-07-12 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobapplication', '0006_job_capacity_job_education_level_job_experience_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-submission_time']},
        ),
    ]
