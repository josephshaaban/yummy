from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='blog-about'),
    path('bill/', views.BillCreateView.as_view(), name='bill'),
    path('recent_bills/', views.BillListView.as_view(), name='recent_bills'),
    path('inventory/', views.InventoryCreateView.as_view(), name='inventory'),
    path('inventory_log/', views.InventoryLogListView.as_view(), name='inventory_log'),
    
]

