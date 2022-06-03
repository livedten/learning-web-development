from django.db import models
from django.urls import reverse     # Используется для генерации URL-адресов путем отмены шаблонов URL-адреса
import uuid     # Требуется для уникальных экземпляров книги

# Create your models here.


class Genre(models.Model):
    """Модель представляющая жанр книги."""
    name = models.CharField(max_length=200,
                            help_text='Введите жанр книги (например, научная фантастика)',
                            verbose_name='жанр')

    def __str__(self):
        """Строка для представления объекта модели (на сайте администратора и т.д.)."""
        return self.name

    class Meta:
        """Передача метаданных модели"""
        # Опции метаданных модели:
        # https://django.fun/docs/django/ru/4.0/topics/db/models/#meta-options

        # Удобочитаемое имя для объекта, единственное число:
        verbose_name = 'жанр'

        # Имя во множественном числе для объекта:
        verbose_name_plural = 'жанры'


class Book(models.Model):
    """Модель, представляющая книгу (но не конкретную копию книги)."""
    title = models.CharField(max_length=200, verbose_name='заголовок')

    # Используем Foreign Key, потому что в книге может быть только один автор, но у авторов может быть несколько книг
    # 'Author' как строка, а не объект, потому что он еще не был объявлен в файле
    # Аргументы поведения при удалении:
    # https://django.fun/docs/django/ru/4.0/ref/models/fields/#arguments
    # SET_NULL -- устанавливает NULL, возможно только при null=True
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, verbose_name='автор')
    """
    Предупреждение: по умолчанию on_delete=models.CASCADE, что означает, что если автор будет удален, 
    эта книга тоже будет удалена! Мы используем set_null здесь, но мы также могли бы использовать 
    PROTECT или RESTRICT, чтобы предотвратить удаление автора, в то время как любая книга использует ее
    """

    summary = models.TextField(max_length=1000,
                               help_text='Введите краткое описание книги',
                               verbose_name='краткое изложение')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                            help_text='13 символов <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')

    # ManyToManyField используется, потому что жанр может содержать много книг. Книги могут охватывать многие жанры.
    # Класс жанра уже определен, поэтому мы можем указать объект выше.
    genre = models.ManyToManyField(Genre, help_text='Выберите жанр для этой книги', verbose_name='жанр')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True, verbose_name='язык')

    def __str__(self):
        """Строка для представления объекта модели (на сайте администратора и т.д.)."""
        return self.title

    def get_absolute_url(self):
        """Возвращает URL, чтобы получить доступ к подробной записи для этой книги."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Создает строку для жанра. Это необходимо для отображения жанра в Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'жанр'

    class Meta:
        """Передача метаданных модели"""
        # Опции метаданных модели:
        # https://django.fun/docs/django/ru/4.0/topics/db/models/#meta-options

        # Удобочитаемое имя для объекта, единственное число:
        verbose_name = 'книга'

        # Имя во множественном числе для объекта:
        verbose_name_plural = 'книги'


class BookInstance(models.Model):
    """Модель, представляющая конкретную копию книги (то есть, которая может быть заимствована из библиотеки)."""
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          help_text='Уникальный идентификатор этой конкретной книги по всей библиотеке')
    # ForeignKey для идентификации связанной книги (каждая книга может иметь много копий,
    # но копия может иметь только одну книгу).
    # Ключ указывает on_delete=models.RESTRICT, чтобы гарантировать, что книга не может быть удалена,
    # когда на нее ссылается BookInstance.
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True, verbose_name='книга')
    imprint = models.CharField(max_length=200, verbose_name='печать')
    due_back = models.DateField(null=True, blank=True, verbose_name='ожидаемая дата возврата')

    LOAN_STATUS = (
        ('о', 'На обслуживании'),
        ('в', 'Выдана'),
        ('н', 'В наличии'),
        ('р', 'Зарезервирована'),
    )
    status = models.CharField(max_length=1,
                              choices=LOAN_STATUS,
                              blank=True,
                              default='о',
                              help_text='Доступность книги',
                              verbose_name='статус')

    class Meta:
        """Передача метаданных модели"""
        # Опции метаданных модели:
        # https://django.fun/docs/django/ru/4.0/topics/db/models/#meta-options

        # Сортировка по...
        ordering = ['due_back']

        # Удобочитаемое имя для объекта, единственное число:
        verbose_name = 'экземпляр книги'

        # Имя во множественном числе для объекта:
        verbose_name_plural = 'экземпляры книг'

    def __str__(self):
        """Строка для представления объекта модели (на сайте администратора и т.д.)."""
        return '{0} ({1})'.format(self.id, self.book.title)


class Author(models.Model):
    """Модель, представляющая автора."""
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='дата рождения')
    date_of_death = models.DateField('дата смерти', null=True, blank=True)

    class Meta:
        """Передача метаданных модели"""
        # Опции метаданных модели:
        # https://django.fun/docs/django/ru/4.0/topics/db/models/#meta-options

        # Сортировка по...
        ordering = ['last_name', 'first_name']

        # Удобочитаемое имя для объекта, единственное число:
        verbose_name = 'автор'

        # Имя во множественном числе для объекта:
        verbose_name_plural = 'авторы'

    def get_absolute_url(self):
        """Возвращает URL для доступа к конкретному экземпляру автора."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта модели (на сайте администратора и т.д.)."""
        return '{0}, {1}'.format(self.last_name, self.first_name)


class Language(models.Model):
    """Модель представляющая язык книги."""
    name = models.CharField(max_length=200,
                            help_text='Введите на каком языке написана книга (например, Беларуский)',
                            verbose_name='язык')

    def __str__(self):
        """Строка для представления объекта модели (на сайте администратора и т.д.)."""
        return self.name

    class Meta:
        """Передача метаданных модели"""
        # Опции метаданных модели:
        # https://django.fun/docs/django/ru/4.0/topics/db/models/#meta-options

        # Удобочитаемое имя для объекта, единственное число:
        verbose_name = 'язык'

        # Имя во множественном числе для объекта:
        verbose_name_plural = 'языки'
