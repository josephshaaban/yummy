from django.contrib import admin

from blog.models import Bill, Item

admin.site.register(Item)
admin.site.register(Bill)
