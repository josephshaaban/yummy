from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
)
from .models import Bill


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class BillCreateView(CreateView):
    model = Bill

    def form_valid(self, form):
        return super().form_valid(form)


def recent_bills(request):
    context = {
        'bills': Bill.objects.all()
    }
    return render(request, 'blog/recent_bills.html', context)


class BillListView(ListView):
    model = Bill
    template_name = 'blog/recent_bills.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'bills'
    ordering = ['date_posted']

