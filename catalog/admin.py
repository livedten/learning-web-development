from django.contrib import admin
from .models import Author, Genre, Language, Book, BookInstance

# Зарегистрируйте свои модели здесь.

# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(Book)
# admin.site.register(BookInstance)

"""
Интерфейс администратора:
https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
https://django.fun/docs/django/ru/4.0/ref/contrib/admin/

Объекты ModelAdmin:
https://docs.djangoproject.com/en/4.0/ref/contrib/admin/#modeladmin-objects
https://django.fun/docs/django/ru/4.0/ref/contrib/admin/#modeladmin-objects
"""


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


# Определяем класс администратора
class AuthorAdmin(admin.ModelAdmin):

    # Настройка отображения списков:
    # https://django.fun/docs/django/ru/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_display
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    # Настройка в макете форм на страницах «добавить» и «изменить»
    # https://django.fun/docs/django/ru/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fields
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    inlines = [BookInline]


# Зарегистрируйте класс администратора с соответствующей моделью
admin.site.register(Author, AuthorAdmin)


# Встроенное редактирование связанных записей(вставки):
# https://django.fun/docs/django/ru/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.inlines
# https://django.fun/docs/django/ru/4.0/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin
# TabularInline (горизонтальное расположение)
# StackedInline (вертикальное расположение, так же как и в модели по умолчанию)
class BookInstanceInline(admin.TabularInline):
    model = BookInstance

    # Количество дополнительных форм, по умолчанию = 3
    # https://django.fun/docs/django/ru/4.0/ref/contrib/admin/#django.contrib.admin.InlineModelAdmin.extra
    extra = 0


# Зарегистрируйте классы администратора для книги с помощью декоратора
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


# Зарегистрируйте классы администратора для BookInstance с помощью декоратора.
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')

    # Добавление фильтров списка:
    # https://django.fun/docs/django/ru/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter
    list_filter = ('status', 'due_back')

    # Разделение на секции/Выделение подробного представления:
    # https://django.fun/docs/django/ru/4.0/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    #
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Наличие', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
