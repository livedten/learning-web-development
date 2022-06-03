from django.shortcuts import render
from django.http import HttpResponse
from .models import Author, Genre, Language, Book, BookInstance

# Create your views here.

"""
Вспомогательные функции Django:
render(), redirect(), get_object_or_404(), get_list_or_404()
https://docs.djangoproject.com/en/4.0/topics/http/shortcuts/#django.shortcuts.render
https://django.fun/docs/django/ru/4.0/topics/http/shortcuts/#django.shortcuts.render
"""


def index(request):
    """Функция отображения для домашней страницы сайта."""
    # Методы, которые возвращают новый QuerySet:
    # https://django.fun/docs/django/ru/4.0/ref/models/querysets/#methods-that-return-new-querysets
    # Поиск Field:
    # https://django.fun/docs/django/ru/4.0/ref/models/querysets/#field-lookups

    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Доступные книги (статус = 'н')
    num_instances_available = BookInstance.objects.filter(status__exact='н').count()

    # Метод 'all()' применён по умолчанию.
    num_authors = Author.objects.count()

    # Количество жанров и количество книг, которые содержат в своих заголовках какое-либо слово (без учёта регистра)
    num_genres_word = Genre.objects.filter(name__icontains='Роман').count()
    num_books_word = Book.objects.filter(title__icontains='Мастер').count()

    # Отрисовка HTML-шаблона index.html с данными в переменной контекста context
    return render(request, 'catalog/index.html', context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres_word': num_genres_word,
        'num_books_word': num_books_word,
    })


def books(request):
    return HttpResponse("Список всех книг")


def authors(request):
    return HttpResponse("Список всех авторов")


def book(request):
    return HttpResponse("Детальная информация для определённой книги")


def author(request):
    return HttpResponse("Детальная информация для определённого автора")
