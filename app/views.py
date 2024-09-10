from django.db.models import Count, OuterRef, Subquery
from django.shortcuts import render

from app.models import Author, Book

# Create your views here.


# def index(request):
#     # authors = {'authors_count':3}
#     # authors = Author.objects.all().aggregate(max_price_book = Max('price'))
#     count = authors.get('authors_count')
#     return render(request, 'app/index.html', {'count': count})
#
#
# def book_list(request):
#     books = Book.objects.all().annotate(min_price=Max('price')).filter(min_price__gt = 5000).order_by('-min_price').aggregate(avg_book_price=Avg('min_price'))
#     print(books)
#     # expensive_books = Book.objects.filter(author=OuterRef('pk')).values('price').order_by('-price')[:1]
#     # authors = Author.objects.all().annotate(most_expensive_book=Subquery(expensive_books))
#     return render(request, 'app/index.html', {'books': books})
#

#
"""
1) author's => book count
2) author's => max price book
3) author's => min price book
4) author's => min price average

"""


def magic(request):
    # authors = Author.objects.all().annotate(book_count=Count('books'))
    # books = Book.objects.values('author__name').annotate(book_count=Count('id'))
    most_expensive_book = Book.objects.filter(author=OuterRef('pk')).values('price').order_by('-price')[:1]
    authors = Author.objects.annotate(most_popular_book=Subquery(most_expensive_book))
    return render(request, 'app/index.html', {'authors': authors})

#
#
# Book.objects.all().filter()
# Book.objects.




