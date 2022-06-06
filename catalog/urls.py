from django.urls import path, re_path
from . import views

"""
Совет W3C:
https://www.w3.org/Provider/Style/URI

Функции для использования в URL confs:
https://django.fun/docs/django/ru/4.0/ref/urls/#

re - Операции с регулярными выражениями:
https://docs.python.org/3/library/re.html

Передача дополнительных параметров функции предствления:
https://django.fun/docs/django/ru/4.0/topics/http/urls/#views-extra-options
"""

urlpatterns = [
    path('', views.index, name='index'),   # Главная/индексная страница
    path('books/', views.BookListView.as_view(), name='books'),   # Список всех книг
    # Детальная информация для определённой книги
    # path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    # Детальная информация для определённой книги
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),   # Список всех авторов
    # Детальная информация для определённого автора
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
]
