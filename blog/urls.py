from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='blog-about'),
    path('bill/', views.BillCreateView.as_view(), name='bill'),
]

