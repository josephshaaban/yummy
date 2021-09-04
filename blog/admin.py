from django.contrib import admin
from django.forms import BaseInlineFormSet

from blog.forms import OrderForm
from blog.models import Bill, Item, Order

admin.site.register(Item)
admin.site.register(Order)


class OrderInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()


class OrderInline(admin.StackedInline):
    model = Order
    formset = OrderInlineFormset
    form = OrderForm
    extra = 1


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = [OrderInline, ]
