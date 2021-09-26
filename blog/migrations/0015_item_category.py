# Generated by Django 3.2.6 on 2021-09-25 22:18

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_bill_takeaway'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[(blog.models.ItemCategories['COLD_MEATS'], blog.models.ItemCategories['COLD_MEATS']), (blog.models.ItemCategories['MEATS'], blog.models.ItemCategories['MEATS']), (blog.models.ItemCategories['HAWADER'], blog.models.ItemCategories['HAWADER'])], default='', max_length=40),
            preserve_default=False,
        ),
    ]