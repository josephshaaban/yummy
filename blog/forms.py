from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from django import forms
from django.forms import inlineformset_factory

from dal import autocomplete, forward

from .custom_layout_object import Formset
from .helper_classes import DalAdminFormMixin
from .models import Order, Bill, ItemCategory, Item


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('bill', )
        widgets = {
            'count': forms.NumberInput(attrs={'style': 'width: 80px'}),
            'notes': forms.Textarea(attrs={'cols': '', 'rows': ''}),
        }

    item = forms.ModelChoiceField(
        # queryset is required to show the saved data on field init
        queryset=Item.objects.all(),
        required=True,
        widget=autocomplete.ModelSelect2(
            url='item-autocomplete',
            forward=(
                forward.Field('category', 'category_id'),
            ),
            attrs={
                'class': 'admin-input-select2',
                'data-minimum-input-length': 0,  # initial load of items without typing
                'data-allow-clear': 'true',  # display 'x' in field allowing to clear choice
                'data-placeholder': '',  # set choice to empty when clearing
                'style': 'width: 100%',
                'data-dropdown-auto-width': 'true',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        try:
            bill = kwargs.pop('bill')
        except KeyError:
            bill = None
        super().__init__(*args, **kwargs)
        self._bill = bill

    def save(self, commit=True):
        self.instance.bill = self._bill
        return super().save(commit=commit)


class BillModelForm(DalAdminFormMixin, forms.ModelForm):
    # todo: exclude and validate date_posted
    class Meta:
        model = Bill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # do not insert the form tag, since we are bundling multiple forms
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        # self.helper.layout = Layout(
        #     Div(
        #         Field('client_name'),
        #         Field('date_posted'),
        #         Field('delivery'),
        #         Field('takeaway'),
        #         Fieldset(
        #             '',
        #             Formset('orders'),
        #             css_class='orders-fieldset'
        #         ),
        #         HTML("<br>"),
        #         ButtonHolder(Submit('submit', 'save')),
        #         )
        #     )


OrderInlineFormSet = inlineformset_factory(Bill, Order, OrderModelForm, fields='__all__', extra=1)
