import csv
import datetime
import json
import openpyxl
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

            return redirect('customer_details', customer.slug)


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
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    format = request.GET.get('format')
    if format == 'csv':
        meta = Customer._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')

        response['Content-Disposition'] = f'attachment; filename={Customer._meta.object_name}-{date}.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in Customer.objects.all():
            writer.writerow([getattr(obj, field) for field in field_names])


    elif format == 'json':
        response = HttpResponse(content_type='application/json')
        data = list(Customer.objects.all())
        response.write(json.dumps(data, indent=4, default=str))
        response['Content-Disposition'] = f'attachment; filename={Customer._meta.object_name}-{date}.json'




    elif format == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.xlsx"'
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = 'Customers'
        header = ['ID', 'Full Name', 'Email', 'Addres', 'Slug', 'Phone Number']

        worksheet.append(header)
        customers = Customer.objects.all()
        for obj in customers:
            worksheet.append([obj.id, obj.full_name, obj.email, obj.address, obj.slug, obj.phone])

        workbook.save(response)
        return response

    # header

    else:
        response = HttpResponse(status=404)
        response.content = 'Bad Request'

    return response


class ExportData(View):
    def get(self, request):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        format = request.GET.get('format')
        if format == 'csv':
            meta = Customer._meta
            field_names = [field.name for field in meta.fields]
            response = HttpResponse(content_type='text/csv')

            response['Content-Disposition'] = f'attachment; filename={Customer._meta.object_name}-{date}.csv'
            writer = csv.writer(response)
            writer.writerow(field_names)
            for obj in Customer.objects.all():
                writer.writerow([getattr(obj, field) for field in field_names])


        elif format == 'json':
            response = HttpResponse(content_type='application/json')
            data = list(Customer.objects.all())
            response.write(json.dumps(data, indent=4, default=str))
            response['Content-Disposition'] = f'attachment; filename={Customer._meta.object_name}-{date}.json'




        elif format == 'xlsx':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{Customer._meta.object_name}-{date}.xlsx"'
            workbook = openpyxl.Workbook()
            worksheet = workbook.active
            worksheet.title = 'Customers'
            header = ['ID', 'Full Name', 'Email', 'Addres', 'Slug', 'Phone Number']

            worksheet.append(header)
            customers = Customer.objects.all()
            for obj in customers:
                worksheet.append([obj.id, obj.full_name, obj.email, obj.address, obj.slug, obj.phone])

            workbook.save(response)
            return response

        # header

        else:
            response = HttpResponse(status=404)
            response.content = 'Bad Request'

        return response
