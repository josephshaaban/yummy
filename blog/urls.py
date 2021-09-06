from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='blog-about'),
    path('bill/', views.BillCreateView.as_view(), name='bill'),
    path('create_order/', views.OrderCreateView.as_view(), name='create_order'),
    path('manage_bill/<int:pk>/', views.add_orders_view, name='manage_bill'),
    path('add_orders/', views.add_orders_view, name='add_orders'),

    path('bill/<int:pk>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('bill/create/', views.BillCreate.as_view(), name='bill_create'),
    path('bill/update/<int:pk>/', views.BillUpdate.as_view(), name='bill_update'),
    path('bill/delete/<int:pk>/', views.BillDelete.as_view(), name='bill_delete'),
    path('bill/list/', views.BillList.as_view(), name='bill_list')

]

