from django.urls import path
from . import views

"""
Совет W3C:
https://www.w3.org/Provider/Style/URI

Функции для использования в URL confs:
https://django.fun/docs/django/ru/4.0/ref/urls/#
"""
urlpatterns = [
    path('', views.index, name='index'),   # Главная/индексная страница
    path('books/', views.books),   # Список всех книг
    path('authors/', views.authors),   # Список всех авторов
    path('book/<id>', views.book),   # Детальная информация для определённой книги
    path('author/<id>', views.author),   # Детальная информация для определённого автора
]
