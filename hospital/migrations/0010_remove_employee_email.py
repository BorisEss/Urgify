# Generated by Django 4.0.5 on 2022-10-16 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0009_alter_department_name_alter_employee_attribution_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
    ]
