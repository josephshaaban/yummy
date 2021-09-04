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
    double_price = models.PositiveIntegerField(blank=True, null=True)
    meal_price = models.PositiveIntegerField(blank=True, null=True)
    double_meal_price = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Bill(models.Model):
    client_name = models.CharField(
        max_length=50,
        blank=False, null=False,
    )
    date_posted = models.DateTimeField(default=timezone.now)
    delivery = models.BooleanField(default=False)

    @property
    def cost(self):
        cost_ = 0
        for order in self.orders.all():
            cost_ += order.price
        return cost_

    def __str__(self):
        return f'{self.client_name}, cost: {self.cost}'


class Order(models.Model):
    item = models.ForeignKey(
        Item,
        models.PROTECT,
        related_name='orders',
        blank=False, null=False,
    )
    count = models.PositiveIntegerField(default=1)
    double = models.BooleanField(default=False)
    meal = models.BooleanField(default=False)
    notes = models.TextField(
        blank=True, null=True,
    )
    bill = models.ForeignKey(
        Bill,
        models.PROTECT,
        related_name='orders',
        blank=True, null=True,
    )

    @property
    def price(self):
        count_ = int(self.count)
        if self.double and self.meal:
            return count_ * self.item.double_meal_price
        if self.meal:
            return count_ * self.item.meal_price
        if self.double:
            return count_ * self.item.double_price

        return count_ * self.item.item_price

    def __str__(self):
        # item_ = Item.objects.get(item=self.item)
        str_ = str(self.item)
        # str_ = ''
        if self.double:
            str_ += ', double'
        if self.meal:
            str_ += ' meal'
        str_ += f', {self.price}'
        return str_
