from django.apps import AppConfig


class CatalogConfig(AppConfig):
    # Конфигурация приложения:
    # https://django.fun/docs/django/ru/4.0/ref/applications/#django.apps.AppConfig.verbose_name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'

    # Человекочитаемое имя приложения
    verbose_name = 'каталог'
