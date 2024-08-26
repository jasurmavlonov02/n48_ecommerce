import csv
import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View

from my_web.models import Customer
from my_web.forms import CustomerModelForm


# Create your views here.


def project_management(request):
    return render(request, 'my_web/project-management.html')


# def customers(request):
#     search = request.GET.get('search')
#     filter_date = request.GET.get('filter', '')
#     customers = Customer.objects.all()
#     if search:
#         customers = customers.filter(Q(full_name__icontains=search) | Q(email__icontains=search))
#     if filter_date == 'filter_date':
#         customers = customers.order_by('-created_at')
#     context = {'customers': customers}
#     return render(request, 'my_web/customers.html', context)
#

class CustomerListView(View):
    def get(self, request):
        search = request.GET.get('search')
        filter_date = request.GET.get('filter', '')
        customers = Customer.objects.all()
        for customer in customers:
            print(customer.full_name, customer.email)
        if search:
            customers = customers.filter(Q(full_name__icontains=search) | Q(email__icontains=search))
        if filter_date == 'filter_date':
            customers = customers.order_by('-created_at')
        context = {'customers': customers}
        return render(request, 'my_web/customers.html', context)


# def customer_details(request, customer_slug):
#     customer = Customer.objects.get(slug=customer_slug)
#     context = {'customer': customer}
#     return render(request, 'my_web/customer-details.html', context)

class CustomerDetailView(View):
    def get(self, request, *args, **kwargs):
        customer_slug = kwargs['customer_slug']
        print(args)
        print(kwargs)
        customer = Customer.objects.get(slug=customer_slug)
        # customer = Customer.objects.raw('''select * from customer where slug=%s''', [customer_slug])
        context = {'customer': customer}
        return render(request, 'my_web/customer-details.html', context)


def profile(request):
    return render(request, 'my_web/profile.html')


def profile_settings(request):
    return render(request, 'my_web/settings.html')


#
# def add_customer(request):
#     form = CustomerModelForm()
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#
#     context = {'form': form}
#
#     return render(request, 'my_web/add-customer.html', context)


class CustomerCreateView(View):
    def get(self, request):
        form = CustomerModelForm()
        return render(request, 'my_web/add-customer.html', {'form': form})

    def post(self, request):
        form = CustomerModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customers')


# def edit_customer(request, customer_slug):
#     customer = get_object_or_404(Customer, slug=customer_slug)
#     form = CustomerModelForm(instance=customer)
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST, request.FILES, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('customers', )
#     return render(request, 'my_web/settings.html', {'form': form, 'customer': customer})


class CustomerUpdateView(View):
    def get(self, request, customer_slug):
        customer = get_object_or_404(Customer, slug=customer_slug)
        form = CustomerModelForm(instance=customer)
        return render(request, 'my_web/settings.html', {'form': form, 'customer': customer})

    def post(self, request, customer_slug):
        customer = get_object_or_404(Customer, slug=customer_slug)
        form = CustomerModelForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_details', customer_slug)


# def delete_customer(request, customer_slug):
#     customer = get_object_or_404(Customer, slug=customer_slug)
#     if customer:
#         customer.delete()
#         return redirect('customers')


class CustomerDeleteView(View):
    def get(self, request, customer_slug):
        customer = get_object_or_404(Customer, slug=customer_slug)
        if customer:
            customer.delete()
            return redirect('customers')


def export_data(request):
    format = request.GET.get('format')
    if format == 'csv':
        meta = Customer._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        response['Content-Disposition'] = f'attachment; filename={Customer._meta.object_name}-{date}.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in Customer.objects.all():
            writer.writerow([getattr(obj, field) for field in field_names])


    elif format == 'json':
        response = None


    elif format == 'xlsx':
        response = None


    return response
