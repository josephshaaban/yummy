# Generated by Django 3.2.6 on 2021-09-20 15:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20210915_2220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element', models.CharField(max_length=40)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
