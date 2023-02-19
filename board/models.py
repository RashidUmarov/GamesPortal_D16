from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from ckeditor.fields import RichTextField


# автор объявления или отклика
class Author(models.Model):
    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    author = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')
    is_subscriber = models.BooleanField(verbose_name='Подписчик', default=False)

    def __str__(self):
        if self.full_name:
            return f'{self.full_name}'
        else:
            return str(self.author)


# категория объявления
class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    TYPE = ['Танки',
            'Хилы',
            'ДД',
            'Торговцы',
            'Гилдмастеры',
            'Квестгиверы',
            'Кузнецы',
            'Кожевники',
            'Зельевары',
            'Мастера заклинаний',
            ]
    name = models.CharField(max_length=20,
                            help_text='Категории объявлений',
                            verbose_name='Категория', unique=True)

    def __str__(self):
        return self.name


# объявление
class Post(models.Model):
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = RichTextField(config_name='default')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    attach = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True, verbose_name='Вложение')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


# отклик на объявление
class Response(models.Model):
    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявление')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text[0:30]}'
