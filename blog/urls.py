from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path(
        'bill/',
        views.BillList.as_view(),
        name='bill_list',
    ),
    path(
        'bill/list/refresh',
        views.BillList.as_view(template_name='blog/bill_list_refresh.html'),
        name='bill_list_refresh',
    ),
    path('about/', views.about, name='blog-about'),
    path('bill/<int:pk>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('', views.BillCreate.as_view(), name='bill_create'),
    path('bill/update/<int:pk>/', views.BillUpdate.as_view(), name='bill_update'),
    path('bill/delete/<int:pk>/', views.BillDelete.as_view(), name='bill_delete'),
    path('inventory/', views.InventoryCreateView.as_view(), name='inventory'),
    path('inventory_log/', views.InventoryLogListView.as_view(), name='inventory_log'),
    path('bill/item/items_dropdown_options/<str:category>', views.items_dropdown, name='items_dropdown_options'),

]

