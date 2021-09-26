from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (
    ListView,
    UpdateView, DetailView, DeleteView,
    CreateView,
)

from .forms import OrderForm, BaseOrderFormSet, BillModelForm, OrderInlineFormSet, BillForm
from .models import Bill, Order, Inventory


def home(request):
    return render(request, 'blog/home.html', {'title':'home'})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class OrderCreateView(CreateView):
    model = Order
    fields = '__all__'
    template_name = 'blog/bill_form.html'

    def form_valid(self, form):
        return super().form_valid()


class BillCreateView(CreateView):
    model = Bill
    fields = '__all__'

    def form_valid(self, form):
        return super().form_valid(form)


class BillListView(ListView):
    model = Bill
    template_name = 'blog/recent_bills.html'
    context_object_name = 'bills'
    ordering = ['date_posted']


def add_orders_view(request, pk=False):
    if pk:
        bill = Bill.objects.get(
            pk=pk)  # if this is an edit form, replace the author instance with the existing one
    else:
        bill = Bill()
    bill_form = BillModelForm(instance=bill)  # setup a form for the parent

    formset = OrderInlineFormSet(instance=bill)

    if request.method == 'POST':
        bill_form = BillModelForm(request.POST)
        if pk:
            bill_form = BillModelForm(request.POST, instance=bill)

        formset = OrderInlineFormSet(request.POST, request.FILES)
        if bill_form.is_valid():
            create_bill = bill_form.save(commit=False)
            formset = OrderInlineFormSet(request.POST, request.FILES, instance=create_bill)

            if formset.is_valid():
                create_bill.save()
                formset.save()
                return HttpResponseRedirect(create_bill.get_absolute_url())
            # formset.save()
    # else:
    #     formset = OrderFormSet(instance=bill)
    #     # formset = OrderFormSet()
    return render(
        request, 'blog/add_orders.html', {
            'bill_form': bill_form,
            'formset': formset,
        })


class BillDetailView(DetailView):
    model = Bill
    template_name = 'blog/bill_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class BillCreate(CreateView):
    model = Bill
    template_name = 'blog/bill_create.html'
    form_class = BillForm
    success_url = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.object = form.instance

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs.setdefault('view', self)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        if self.request.POST:
            kwargs['orders'] = OrderInlineFormSet(self.request.POST)
            kwargs['date_posted'] = timezone.now()
        else:
            kwargs['orders'] = OrderInlineFormSet()
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        orders = context['orders']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            # self.object = form.instance.create()
            self.object = form.save(commit=True)
            self.object.save()
            if orders.is_valid():
                for order in orders:
                    # order_ = order.save()
                    order.instance.bill = self.object
                    order.save()
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bill_create')

    # def get(self, request, *args, **kwargs):
    #     return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        # form.data['date_posted'] = timezone.now()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BillUpdate(UpdateView):
    model = Bill
    template_name = 'blog/bill_create.html'
    form_class = BillForm
    success_url = ''

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['orders'] = OrderInlineFormSet(self.request.POST, instance=self.object)
        else:
            data['orders'] = OrderInlineFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orders = context['orders']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if orders.is_valid():
                orders.bill = self.object
                orders.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bill_detail', kwargs={'pk': self.object.pk})


class BillDelete(DeleteView):
    model = Bill
    template_name = 'blog/confirm_delete.html'
    success_url = reverse_lazy('blog:home')


class BillList(ListView):
    model = Bill
    ordering = 'date_posted'
    template_name = 'blog/bill_list.html'


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
    ordering = ['-timestamp']