"""A mixin class for admin form classes that use django-autocomplete-light"""
from django import forms


class DalAdminFormMixin:  # pylint: disable=R0903
    """
    A Mixin class that can be inherited in admin form classes that use django-autocomplete-light
    Select2 widgets. The mixin aims to workaround a js load order issue in the library.
    Refer to https://github.com/yourlabs/django-autocomplete-light/issues/1137 for details.
    """
    @property
    def media(self):
        """
        Override parent media property to insert the additional js files.
        Note that both files should have been already inserted into any admin form that uses a
        django-autocomplete-light Select2 widget (regardless of whether this mixin is used).
        The aim of providing them here is to force django to load them in the correct order.
        """
        return super().media + forms.Media(
            js=[
                # inserted by django-admin into any admin page
                'admin/js/jquery.init.js',
                # inserted by django-autocomplete-light into Select2 widgets
                'autocomplete_light/jquery.init.js',
            ],
        )
