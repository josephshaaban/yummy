# Generated by Django 3.2.6 on 2021-09-04 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210904_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='orders',
        ),
        migrations.AddField(
            model_name='order',
            name='bill',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='blog.bill'),
        ),
    ]