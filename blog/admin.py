from django.contrib import admin
from django.forms import BaseInlineFormSet

from .forms import OrderForm, OrderInlineFormSet, OrderModelForm
from .models import Bill, Item, Order, ItemCategory

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(ItemCategory)

# class OrderInlineFormset(BaseInlineFormSet):
#     def clean(self):
#         super().clean()


class OrderInline(admin.StackedInline):
    model = Order
    # formset = OrderInlineFormset
    formset = OrderInlineFormSet
    form = OrderForm
    extra = 1


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = [OrderInline, ]
