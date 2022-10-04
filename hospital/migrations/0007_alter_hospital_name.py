# Generated by Django 4.0.5 on 2022-10-02 05:01

from django.db import migrations
import hospital.fields


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_alter_department_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='name',
            field=hospital.fields.CaseInsensitiveCharField(max_length=255, unique=True),
        ),
    ]
