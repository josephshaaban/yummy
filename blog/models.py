from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.utils import timezone


class Item(models.Model):
    name = models.CharField(
        max_length=40,
        blank=False, null=False,
    )
    item_price = models.PositiveIntegerField(
        blank=False, null=False,
    )
    double_price = models.PositiveIntegerField(
        blank=False, null=False,
    )
    meal_price = models.PositiveIntegerField(
        blank=False, null=False,
    )
    double_meal_price = models.PositiveIntegerField(
        blank=False, null=False,
    )


class Order(models.Model):
    item = models.ForeignKey(
        Item,
        models.PROTECT,
        related_name='items',
        blank=False, null=False,
    )
    count = models.PositiveIntegerField(default=1)
    double = models.BooleanField(default=False)
    meal = models.BooleanField(default=False)
    notes = models.TextField(
        blank=True, null=True,
    )

    @property
    def price(self):
        item_price = 0
        try:
            item_ = Item.objects.get(item=self.item)
            if self.double and self.meal:
                item_price = item_.double_meal_price
            if self.meal:
                item_price = item_.meal_price
            if self.double:
                item_price = item_.double_price

            item_price = item_.item_price
            return item_price * self.count
        except ObjectDoesNotExist:
            return item_price
        except MultipleObjectsReturned:
            return item_price


class Bill(models.Model):
    # TODO: add delivery Boolean field and address CharField.
    purchase = models.ManyToManyField(
        Order,
        related_name='orders',
        blank=False,
    )
    client_name = models.CharField(
        max_length=50,
        blank=False, null=False,
    )
    date_posted = models.DateTimeField(default=timezone.now)

    @property
    def cost(self):
        cost_ = 0
        # TODO: iterate on all orders
        for order in self.purchase:
            cost_ += order.total
        return cost_


class Inventory(models.Model):
    element = models.CharField(
        max_length=40,
        blank=False, null=False,
    )
    price = models.PositiveIntegerField(
        blank=False, null=False,
    )
    quantity = models.CharField(
        max_length = 50,
        blank=False, null=False,
    )
    timestamp = models.DateTimeField(default=timezone.now)
