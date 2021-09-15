from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('bill/', views.BillList.as_view(), name='bill_list'),
    path('about/', views.about, name='blog-about'),
    path('bill/<int:pk>/', views.BillDetailView.as_view(), name='bill_detail'),
    path('bill/create/', views.BillCreate.as_view(), name='bill_create'),
    path('bill/update/<int:pk>/', views.BillUpdate.as_view(), name='bill_update'),
    path('bill/delete/<int:pk>/', views.BillDelete.as_view(), name='bill_delete'),
]

