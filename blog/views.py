from django.shortcuts import render, reverse
from django.views.generic import (
    ListView,
    CreateView,
)
from .models import Bill, Inventory


def home(request):
    return render(request, 'blog/home.html', {'title':'home'})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class BillCreateView(CreateView):
    model = Bill
    fields = ['date_posted', 'client_name']

    def form_valid(self, form):
        return super().form_valid(form)


class BillListView(ListView):
    model = Bill
    template_name = 'blog/recent_bills.html'
    context_object_name = 'bills'
    ordering = ['date_posted']


class InventoryCreateView(CreateView):
    model = Inventory
    fields = ['element', 'price', 'quantity', 'timestamp']

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('inventory_log')


class InventoryLogListView(ListView):
    model = Inventory
    template_name = 'blog/inventory_log.html'
    context_object_name = 'inventory_log'
    ordering = ['timestamp']
