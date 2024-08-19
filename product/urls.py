from django.contrib import admin
from django.urls import path

from product import views

urlpatterns = [

    path('product-list/', views.ProductListView.as_view(), name='product_list'),

]
