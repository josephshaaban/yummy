from django.contrib import admin
from django.forms import BaseInlineFormSet

from .forms import OrderInlineFormSet, OrderModelForm
from .models import Bill, Item, Order, ItemCategory

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(ItemCategory)


class OrderInline(admin.StackedInline):
    model = Order
    formset = OrderInlineFormSet
    form = OrderModelForm
    extra = 1


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = [OrderInline, ]
