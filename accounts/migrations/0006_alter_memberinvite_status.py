# Generated by Django 4.0.5 on 2022-10-23 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_memberinvite_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberinvite',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Expired'), (4, 'Declined')], default=1),
        ),
    ]