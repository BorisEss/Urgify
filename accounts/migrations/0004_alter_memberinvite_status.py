# Generated by Django 4.0.5 on 2022-10-16 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_memberinvite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberinvite',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Invited'), (2, 'Accepted'), (3, 'Expired'), (4, 'Declined')]),
        ),
    ]
