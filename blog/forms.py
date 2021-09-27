from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms
from django.forms import inlineformset_factory

from .custom_layout_object import Formset
from .models import Order, Bill


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self)

    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'count': forms.Select(attrs={
                'width': 'auto'
            }),
            'double': forms.CheckboxInput(attrs={'class': 'checkboxinput custom-control-input'}),
            'meal': forms.CheckboxInput(attrs={'class': 'checkboxinput custom-control-input'}),
            'notes': forms.Textarea(attrs={
                'cols': '30', 'rows': '5', 'class': 'round-0'
            })

        }


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        widgets = {
            'count': forms.NumberInput(attrs={'style': 'width: 80px'}),
            'notes': forms.Textarea(attrs={'cols': '', 'rows': ''}),
        }


class BillModelForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = '__all__'


class BillForm(forms.ModelForm):
    # todo: exclude and validate date_posted
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
                Field('takeaway'),
                Fieldset(
                    '',
                    Formset('orders'),
                    css_class='orders-fieldset'
                ),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )

    # def clean(self):
    #     cleaned_data = super().clean()
    #     cleaned_data['date_posted'] = timezone.now()
    #
    #     return cleaned_datax`


class BaseOrderFormSet(forms.BaseInlineFormSet):
    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        if queryset is None:
            queryset = Order.objects.none()
        super().__init__(
            data, files, instance, save_as_new, prefix, queryset, **kwargs,
        )


OrderInlineFormSet = inlineformset_factory(Bill, Order, OrderModelForm, fields='__all__', extra=1)
