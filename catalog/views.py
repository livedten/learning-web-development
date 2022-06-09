from django.shortcuts import render
from django.http import HttpResponse
from .models import Author, Genre, Language, Book, BookInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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

    # Как использовать сессии:
    # https://django.fun/docs/django/ru/4.0/topics/http/sessions/
    # Количество посещений этого представления, подсчитанное в переменной сеанса.

    num_visits = request.session.get('num_visits', 0)

    # Подбор числового окончания "раз" = True  или "раза" = False
    def the_ending():
        value = num_visits % 10
        if value == 2 or value == 3 or value == 4:
            request.session['num_visits'] = num_visits + 1
            return False
        return True

    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными в переменной контекста context
    return render(request, 'catalog/index.html', context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres_word': num_genres_word,
        'num_books_word': num_books_word,
        'num_visits': num_visits,
        'the_ending': the_ending,
    })


# Встроенный API представлений на основе классов:
# https://django.fun/docs/django/ru/4.0/ref/class-based-views/
# https://ccbv.co.uk/
# Общие представления на основе классов - упрощенный индекс:
# https://django.fun/docs/django/ru/4.0/ref/class-based-views/flattened-index/#ListView
class BookListView(generic.ListView):
    """Представление просмотра списка"""
    model = Book
    # Ваше собственное имя для списка в качестве переменной шаблона
    context_object_name = 'book_list'
    # Получите 5 книг, содержащих жанр 'Мастер' в заголовке
    # queryset = Book.objects.filter(title__icontains='Мастер')[:5]
    # Укажите собственное имя/местоположение шаблона
    template_name = 'catalog/book_list.html'
    # Постраничный вывод (Pagination)
    paginate_by = 3

    def get_queryset(self):
        # Получите список всех книг
        return Book.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'Это просто некоторые данные'
        return context


class BookDetailView(generic.DetailView):
    """Представление подробного вида"""
    model = Book


class AuthorListView(generic.ListView):
    """Представление просмотра списка"""
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(generic.DetailView):
    """Представление подробного вида"""
    model = Author


# Тестирование проверки подлинности пользователей
# Тестирование в представления
# https://django.fun/docs/django/ru/4.0/topics/auth/default/#limiting-access-to-logged-in-users
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Общий список книг на основе классов, предоставленных текущему пользователю."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='в').order_by('due_back')


class LoanedBooksByStaffListView(PermissionRequiredMixin, generic.ListView):
    """Проверка разрешений на основе класса, предоставленных текущему сотруднику."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_book_borrowed_staff.html'
    paginate_by = 10
    # Разрешения
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='в').order_by('due_back')
