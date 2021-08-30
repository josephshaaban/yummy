from django.contrib import admin

from blog.models import Bill, Item, Order

admin.site.register(Item)
admin.site.register(Bill)
admin.site.register(Order)
