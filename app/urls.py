from django.urls import path

from app import views

urlpatterns = [
    path('', views.book_list, name='book_list')
]
