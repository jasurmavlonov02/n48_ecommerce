from django.shortcuts import render
from django.core.paginator import Paginator
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, DetailView

from product.models import Product


# Create your views here.


# def product_list(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 3)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'products': page_obj
#     }
#     return render(request, 'product/product-list.html', context)


class ProductListView(View):
    def get(self, request):
        products = Product.objects.all()
        paginator = Paginator(products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {
            'products': page_obj
        }
        return render(request, 'product/product-list.html', context)


# ListView , CreateView, DeleteView, UpdateView


# git push -f origin master


class ProductListTemplateView(TemplateView):
    template_name = 'product/product-list.html'

    def get_context_data(self, **kwargs):
        context = super(ProductListTemplateView, self).get_context_data(**kwargs)
        products = Product.objects.all()
        paginator = Paginator(products, 3)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context['products'] = page_obj
        return context


class ProductDetailView(DetailView):
    template_name = 'product/product-detail.html'
    model = Product
    context_object_name = 'product'









