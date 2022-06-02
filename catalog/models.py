from django.db import models
from django.urls import reverse

# Create your models here.


class MyModelName(models.Model):
    """Типичный класс, определяющий модель, полученный из класса модели."""

    # Поля
    my_field_name = models.CharField(max_length=20, help_text='Введите полевую документацию',
                                     verbose_name='мое поле имя')
    # ...
    """
    Указывает, что максимальная длина значения в этом поле составляет 20 символов.
    
    Предоставляет текстовую метку для отображения, чтобы помочь пользователям узнать, 
    какое значение необходимо предоставить, когда это значение должно быть введено пользователем 
    через HTML-форму.
    
    По умолчанию my_field_name будет иметь метку My field name, удобочитаемое имя для поля 
    verbose_name не должно начинаться с заглавной буквы первой буквы.
    
    Опции полей:
    https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-options
    https://django.fun/docs/django/ru/4.0/ref/models/fields/#field-options
    
    Типы полей:
    https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-types
    https://django.fun/docs/django/ru/4.0/ref/models/fields/#field-types
    
    Поля отношений:
    https://docs.djangoproject.com/en/4.0/ref/models/fields/#module-django.db.models.fields.related
    https://django.fun/docs/django/ru/4.0/ref/models/fields/#module-django.db.models.fields.related
    
    OneToOneField - один к одному(например, человек в стране имеет конкретный номер id num паспорта,
    конкретный id принадлежит одному человеку). Table A(Records) -> Table B(Records)
    
    ForeignKey - один ко многим(например, автомобиль имеет одного производителя, но производитель 
    может делать много автомобилей). Table A(Records) -> Table B(Records1, Records2, Records3)
    (например, по одному адресу проживает несколько людей, но один человек имеет один адрес)
    
    ManyToManyField - многие ко многим(например, книга может иметь несколько жанров, и каждый жанр 
    может содержать несколько книг)
    (например, у одного доктора может быть множество пациентов, у пациента может быть несколько 
    докторов)
    """

    # Метаданные
    class Meta:
        ordering = ['-my_field_name']
        verbose_name = "Name"
        verbose_name_plural = 'Names'
    """
    Управление сортировка записей, возвращаемых при запросе типа модели.
    
    verbose_name, подробное имя для класса в единственной и множественной форме
    Если не задано, Django будет использовать verbose_name + "s"
    
    Мета-параметры модели(Опции модели Meta):
    https://docs.djangoproject.com/en/4.0/ref/models/options/#model-meta-options
    https://django.fun/docs/django/ru/4.0/ref/models/options/#model-meta-options
    """

    # Методы
    def get_absolute_url(self):
        """Возвращает URL, чтобы получить доступ к конкретному экземпляру MyModelName."""
        return reverse('model-detail-view', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта MyModelName (на сайте администратора и т.д.)."""
        return self.my_field_name
    """
    Методы модели:
    https://django.fun/docs/django/ru/4.0/ref/models/instances/#django.db.models.Model
    """


"""Создание и изменение записей"""
# Создайте новую запись, используя конструктор модели.
a_record = MyModelName(my_field_name="Instance #1")

# Сохраните объект в базу данных.
a_record.save()

# Доступ к значениям поля модели с использованием атрибутов Python.
print(a_record.id)  # должен вернуть 1 для первой записи.
print(a_record.my_field_name)   # должен распечатать 'Экземпляр #1'

# Изменить запись, изменяя поля, а затем вызывая save().
a_record.my_field_name = "Новое имя экземпляра"
a_record.save()

"""Поиск записей"""
all_books = MyModelName.objects.all()
wild_books = MyModelName.objects.filter(title__contains='wild')
number_wild_books = MyModelName.objects.filter(title__contains='wild').count()

"""
Методы, которые возвращают новый QuerySet:
https://docs.djangoproject.com/en/4.0/ref/models/querysets/#methods-that-return-new-querysets
https://django.fun/docs/django/ru/4.0/ref/models/querysets/#methods-that-return-new-querysets


Поиск по полю(Поиск Field):
https://docs.djangoproject.com/en/4.0/ref/models/querysets/#field-lookups
https://django.fun/docs/django/ru/4.0/ref/models/querysets/#field-lookups
"""