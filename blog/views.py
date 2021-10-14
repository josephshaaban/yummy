from crispy_forms.helper import FormHelper
from dal import autocomplete
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db import transaction
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    ListView,
    UpdateView, DetailView, DeleteView,
    CreateView,
)

from .forms import OrderInlineFormSet, BillModelForm, OrderModelForm
from .models import Bill, Order, Inventory, Item


def home(request):
    return render(request, 'blog/home.html', {'title': 'home'})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class OrderCreateView(CreateView):
    model = Order
    fields = '__all__'
    template_name = 'blog/bill_form.html'

    def form_valid(self, form):
        return super().form_valid()


class BillListView(ListView):
    model = Bill
    template_name = 'blog/recent_bills.html'
    context_object_name = 'bills'
    ordering = ['date_posted']
    queryset = Bill.objects.filter(ready=False)


# todo: remove this function
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


def items_dropdown(request, category):
    items = Item.objects.filter(category=category).values('pk', 'name')
    return render(request, 'blog/items_dropdown_options.html', {'items': items})


class BillCreate(CreateView):
    model = Bill
    template_name = 'blog/bill_create.html'
    form_class = BillModelForm
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
        data = self.request.POST or None
        order_formset = OrderInlineFormSet(self.request.POST, prefix='orders')
        order_formset_helper = FormHelper()
        # use tabular formset for the template
        order_formset_helper.template = 'bootstrap4/table_inline_formset.html'
        # do not insert the form tag, since we are bundling multiple forms
        order_formset_helper.form_tag = False
        # inject the helper into the formset
        order_formset.helper = order_formset_helper
        if self.request.POST:
            kwargs['date_posted'] = timezone.now()
        kwargs['orders'] = order_formset
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
    form_class = BillModelForm
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
    queryset = Bill.objects.filter(ready=False)


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


# View for autocomplete feature
class ItemAutocomplete(autocomplete.Select2QuerySetView):
    """
    Autocomplete view for type Item
    """
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
        #     return Item.objects.none()

        category_id = self.forwarded.get('category_id', None)
        if not category_id:
            q_s = Item.objects.all()
        else:
            q_s = Item.objects.filter(category_id=category_id).distinct()

        if self.q:
            q_s = q_s.search(query=self.q)

        return q_s


class CreateBillView(View):
    @staticmethod
    def create_bill_form(bill_instance=None, data=None):
        return BillModelForm(data=data, instance=bill_instance)

    @staticmethod
    def create_order_formset(bill=None, data=None):
        order_formset_type = modelformset_factory(Order, form=OrderModelForm,
                                                  extra=1, can_delete=True,)
        order_formset = order_formset_type(
            data=data,
            queryset=Order.objects.filter(bill_id=bill),  # pylint: disable=E1101
            form_kwargs=dict(bill=bill),
            prefix='orders',
        )
        order_formset_helper = FormHelper()
        # use tabular formset for the template
        order_formset_helper.template = 'bootstrap4/table_inline_formset.html'
        # do not insert the form tag, since we are bundling multiple forms
        order_formset_helper.form_tag = False
        # inject the helper into the formset
        order_formset.helper = order_formset_helper
        return order_formset

    @staticmethod
    def render_page(request, bill_form, order_formset):
        return render(request, 'blog/bill_creation_form.html', context=dict(
            bill_form=bill_form,
            order_formset=order_formset,
        ))

    def get(self, request, bill_id=None):
        try:
            bill = Bill.objects.get(pk=bill_id)
        except MultipleObjectsReturned:
            return render(request, 'blog/error.html', context=dict(
                error_main="Bill not found",
                error_detail="Your bill does not have an associated Yummy Bill record."
                             "Contact the system administrator for assistance.",
            ))
        except ObjectDoesNotExist:
            bill = None

        bill_form = self.create_bill_form(bill)
        order_formset = self.create_order_formset(bill)
        return self.render_page(request, bill_form, order_formset)

    def post(self, request):
        bill_form = self.create_bill_form(data=request.POST)
        if bill_form.is_valid():
            bill = bill_form.save()
            order_formset = self.create_order_formset(bill=bill, data=request.POST)
            if order_formset.is_valid():
                order_formset.save()
            # messages.success(request, 'Bill details updated.')
            return HttpResponseRedirect(request.path_info)
        order_formset = self.create_order_formset(bill=None, data=request.POST)
        return self.render_page(request, bill_form, order_formset)


def bill_ready_to_deliver(request, pk):
    bill = get_object_or_404(Bill, id=pk)
    bill.ready = True
    bill.save()
    return HttpResponse(status=204)
