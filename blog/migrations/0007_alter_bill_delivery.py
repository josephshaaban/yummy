# Generated by Django 3.2.6 on 2021-09-22 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_bill_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='delivery',
            field=models.PositiveIntegerField(choices=[(500, '500 S.P'), (1000, '1000 S.P'), (1500, '1500 S.P')], default=False),
        ),
    ]