from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms
from django.forms import inlineformset_factory

from blog.custom_layout_object import Formset
from blog.models import Order, Bill


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class BillModelForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'


class BillForm(forms.ModelForm):

    class Meta:
        model = Bill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('client_name'),
                Field('date_posted'),
                Field('delivery'),
                Fieldset(
                    'Add orders',
                    Formset('orders')
                ),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )


class BaseOrderFormSet(forms.BaseInlineFormSet):
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        if queryset is None:
            queryset = Order.objects.none()
        super().__init__(
            data, files, instance, save_as_new, prefix, queryset, **kwargs,
        )


OrderInlineFormSet = inlineformset_factory(Bill, Order, fields='__all__', extra=1)
