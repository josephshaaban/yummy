# Generated by Django 3.2.6 on 2021-09-22 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_bill_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='delivery',
            field=models.PositiveIntegerField(choices=[(0, '0'), (500, '500'), (1000, '1000'), (1500, '1500')], default=0, null=True),
        ),
    ]