from django.contrib import admin
from django.urls import path

from product import views

urlpatterns = [

    path('product-list/', views.ProductListTemplateView.as_view(), name='product_list'),
    path('product-list/<int:pk>/', views.ProductDetailView.as_view(),name='product_detail')

]
