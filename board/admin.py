from django.contrib import admin

from .models import Category, Post, Response, Author


admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Response)
admin.site.register(Author)