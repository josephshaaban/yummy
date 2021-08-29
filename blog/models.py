from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Goods:
    pass


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
    double = models.BooleanField(default=False)
    meal = models.BooleanField(default=False)

    @property
    def price(self):
        if self.double and self.meal:
            return self.double_meal_price
        if self.meal:
            return self.meal_price
        if self.double:
            return self.double_price
        return self.item_price


class Order(models.Model):
    item = models.ForeignKey(
        Item,
        models.PROTECT,
        related_name='items',
        blank=False, null=False,
    )
    count = models.PositiveIntegerField(default=1)
    notes = models.TextField(
        blank=True, null=True,
    )

    @property
    def total(self) -> int:
        try:
            item_ = Item.objects.get(item=self.item)
            return item_.price * self.count
        except ObjectDoesNotExist:
            return 0
        except MultipleObjectsReturned:
            return 0


class Bill(models.Model):
    purchase = models.ManyToManyField(
        Order,
        related_name='orders',
        blank=False, null=False,
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
