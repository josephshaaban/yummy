from django.db import models
from django.utils import timezone


class ItemCategory(models.Model):
    name = models.CharField(max_length=40)

    class Meta:
        verbose_name_plural = "Item Categories"

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT, max_length=40)
    name = models.CharField(
        max_length=40,
        blank=False, null=False,
    )
    item_price = models.PositiveIntegerField(
        blank=False, null=False,
    )
    double_price = models.PositiveIntegerField(default=0,
                                               blank=True, null=True)
    meal_price = models.PositiveIntegerField(default=0,
                                             blank=True, null=True)
    double_meal_price = models.PositiveIntegerField(default=0,
                                                    blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Bill(models.Model):
    client_name = models.CharField(
        max_length=50,
        blank=False, null=False,
    )
    date_posted = models.DateTimeField(default=timezone.now)
    takeaway = models.BooleanField(default=False)
    delivery_CHOICES = [(i, str(i)) for i in [0, 500, 1000, 1500]]
    delivery = models.PositiveIntegerField(null=True,
                                           choices=delivery_CHOICES,
                                           default=0)

    ready = models.BooleanField(default=False, null=True, blank=True)

    @property
    def cost(self):
        cost_ = 0
        for order in self.orders.all():
            cost_ += order.price
        cost_ += self.delivery
        return cost_

    def __str__(self):
        return f'{self.client_name}, cost: {self.cost}'


class Order(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT)
    item = models.ForeignKey(
        Item,
        related_name='orders',
        blank=False, null=False,
        on_delete=models.PROTECT,
    )
    bread_CHOICES = (
        (0, 'خبز'),
        (700, 'مقرنات')
    )
    bread = models.PositiveIntegerField(choices=bread_CHOICES, default=0)
    count = models.PositiveIntegerField(blank=False, default=1)
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
            return count_ * (self.item.double_meal_price + self.bread)
        if self.meal:
            return count_ * (self.item.meal_price + self.bread)
        if self.double:
            return count_ * (self.item.double_price + self.bread)

        return count_ * (self.item.item_price + self.bread)

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
