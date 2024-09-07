from django.shortcuts import render
from django.db.models import Min, Max, Avg, Count, Sum

from app.models import Author, Book


# Create your views here.


def index(request):
    # authors = {'authors_count':3}
    authors = Author.objects.all().aggregate(authors_count=Count('id'))
    count = authors.get('authors_count')
    return render(request, 'app/index.html', {'count': count})


def book_list(request):
    # books = Book.objects.all().annotate(min_price=Max('price')).filter(min_price__gt = 5000).order_by('-min_price').aggregate(avg_book_price=Avg('min_price'))
    # print(books)


    return render(request, 'app/index.html', {'books': books})
