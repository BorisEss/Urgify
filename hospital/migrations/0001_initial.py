# Generated by Django 4.0.5 on 2022-08-11 15:47

import autoslug.fields
from django.db import migrations, models
import hospital.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
                ('logo', models.ImageField(upload_to=hospital.utils.upload_img)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
