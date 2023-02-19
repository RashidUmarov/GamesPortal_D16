from django.shortcuts import redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.contrib.auth.models import User, AnonymousUser

from .models import Post, Response
from .forms import PostForm, ResponseForm
from .models import Author
from GamesPortal.settings import DAILY_POST_LIMIT

class PostsList(ListView):
    queryset = Post.objects.all()
    ordering = '-created'
    template_name = 'board/posts_list.html'
    context_object_name = 'posts'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        prev_day = datetime.utcnow() - timedelta(days=1)
        # количество постов с этого момента
        user = self.request.user
        if not isinstance(self.request.user, AnonymousUser):
            posts_day_count = posts_day_count = Post.objects.filter(created__gte=prev_day, author__author=user).count()
            context['allow_post'] = (posts_day_count < DAILY_POST_LIMIT)
        else:
            context['allow_post'] = False
        context['posts_amount'] = len(self.queryset)
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'board/post.html'
    context_object_name = 'post'

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'

    paginate_by = 10

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = request.user
        if form.is_valid():
            print(f' selected file {request.FILES}')
            post = form.save(commit=False)
            post.author = Author.objects.get_or_create(author=user)[0]
            post.save()
            return self.form_valid(form)
        return redirect('/')


# Добавляем представление для изменения публикации.
class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'board/post_edit.html'


# Представление удаляющее публикацию
class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'board/post_delete.html'
    success_url = reverse_lazy('posts_list')


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/response_add.html'

    success_url = '/board/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = User.objects.get(id=self.request.user.id)
        self.object.post = Post.objects.get(id=self.kwargs.get('pk'))
        self.object.save()
        return super().form_valid(form)


class ResponseDetail(LoginRequiredMixin, UpdateView):
    model = Response
    form_class = ResponseForm
    template_name = 'board/response.html'
    context_object_name = 'post'


def response_approve(request, pk):
    obj = Response.objects.get(id=pk)
    obj.accepted = True
    obj.save()
    return redirect('response_list')

# Представление удаляющее отклик
class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = Response
    template_name = 'board/response_delete.html'
    success_url = reverse_lazy('response_list')


class ResponsesList(LoginRequiredMixin, ListView):
    ordering = '-created'
    template_name = 'board/response_list.html'
    context_object_name = 'posts'

    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['posts_amount'] = len(context['posts'])
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = Response.objects.filter(post__author__author=user)
        return queryset


class UserPosts(ListView):
    queryset = Post.objects.all()
    ordering = '-created'
    template_name = 'board/user_posts.html'
    context_object_name = 'posts'

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['posts_amount'] = len(context['posts'])
        return context

    def get_queryset(self):
        user = self.kwargs.get('pk')
        queryset = Post.objects.filter(author__author=user)
        return queryset
