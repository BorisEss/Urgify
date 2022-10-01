# Generated by Django 4.0.5 on 2022-09-10 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_pay', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preorderpayment',
            name='currency',
            field=models.CharField(choices=[('usd', 'usd')], default='usd', max_length=3),
        ),
        migrations.AlterField(
            model_name='preorderpayment',
            name='payment_method_types',
            field=models.CharField(choices=[('card', 'card')], default='card', max_length=4),
        ),
    ]
