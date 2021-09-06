from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DetailView, DeleteView)

from .forms import OrderForm, BaseOrderFormSet, BillModelForm, OrderInlineFormSet, BillForm
from .models import Bill, Order


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
    success_url = None

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['orders'] = OrderInlineFormSet(self.request.POST)
        else:
            data['orders'] = OrderInlineFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orders = context['orders']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if orders.is_valid():
                orders.instance = self.object
                orders.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bill_detail', kwargs={'pk': self.object.pk})


class BillUpdate(UpdateView):
    model = Bill
    template_name = 'blog/bill_create.html'
    form_class = BillForm
    success_url = None

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
                orders.instance = self.object
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
    template_name = 'blog/bill_list.html'
