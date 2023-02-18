from django import forms
from django.shortcuts import render, redirect

from .models import Post, Response


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            # 'author',
            'category',
            'content',
            'attach',
        ]
        labels = {'title': ('Заголовок'),
                  'content': ('Текст'),
                  'category': ('Категория'),
                  'message_type': ('Тип'),
                  'attach': ('Вложение'),
                  }
        help_texts = {'title': ('Укажите заголовок статьи или поста'),
                      'content': ('Введите текст'),
                      'message_type': ('Выберите тип публикации'),
                      'attach': ('Приложите файл'),
                      'category': ('Укажите категорию ')}


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text',)
