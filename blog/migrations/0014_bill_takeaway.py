# Generated by Django 3.2.6 on 2021-09-24 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_order_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='takeaway',
            field=models.BooleanField(default=False),
        ),
    ]
